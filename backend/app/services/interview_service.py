import json
from datetime import datetime, UTC

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.interview import (
    InterviewStartRequest,
    InterviewAnswerRequest,
)

from app.models.user import User
from app.models.interview_session import InterviewSession
from app.models.interview_question import InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.models.interview_report import InterviewReport
from app.models.interview_feedback import InterviewFeedback
from app.models.career_recommendation import CareerRecommendation

from app.services.interview_context_service import (
    InterviewContextService,
)

from app.services.question_generator import (
    QuestionGenerator,
)

from app.services.answer_evaluator import (
    AnswerEvaluator,
)

from app.services.report_generator import (
    ReportGenerator,
)


class InterviewService:
    """
    Service responsible for managing
    AI mock interview workflows.
    """

    def __init__(self, db: Session):
        self.db = db
        self.answer_evaluator = AnswerEvaluator()

    def _generate_questions_for_session(
        self,
        session: InterviewSession,
    ):
        """
        Generate AI interview questions and save them
        for an existing interview session.
        """

        # -----------------------------------------
        # Build interview context
        # -----------------------------------------

        context_service = InterviewContextService(self.db)

        context = context_service.build_context(
            user_id=session.user_id,
            difficulty=session.difficulty,
        )

        # -----------------------------------------
        # Generate interview questions
        # -----------------------------------------

        generator = QuestionGenerator()

        questions = generator.generate_questions(
            context=context,
            number_of_questions=session.total_questions,
        )

        # -----------------------------------------
        # Save questions
        # -----------------------------------------

        for index, question in enumerate(
            questions,
            start=1,
        ):
            interview_question = InterviewQuestion(
                session_id=session.id,
                question=question["question"],
                category=question["category"],
                difficulty=question["difficulty"],
                question_order=index,
                expected_answer=question.get("expected_answer"),
                generated_by_ai=True,
            )

            self.db.add(interview_question)

        self.db.commit()

        return questions

    def start_interview(
        self,
        user: User,
        data: InterviewStartRequest,
    ):
        """
        Build interview context, generate AI interview
        questions, create an interview session,
        and save generated questions.
        """

        # -----------------------------------------
        # Validate career recommendation
        # -----------------------------------------

        if data.career_recommendation_id is not None:
            recommendation = (
                self.db.query(CareerRecommendation)
                .filter(
                    CareerRecommendation.id == data.career_recommendation_id,
                    CareerRecommendation.user_id == user.id,
                )
                .first()
            )

            if recommendation is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Career recommendation not found.",
                )

        # -----------------------------------------
        # Create interview session
        # -----------------------------------------

        session = InterviewSession(
            user_id=user.id,
            career_recommendation_id=data.career_recommendation_id,
            interview_type=data.interview_type,
            difficulty=data.difficulty,
            total_questions=data.total_questions,
            status="ACTIVE",
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        questions = self._generate_questions_for_session(
            session
        )

        return {
            "session_id": session.id,
            "questions": questions,
        }

    def retry_interview(
        self,
        session_id: int,
        user: User,
    ):
        old_session = (
            self.db.query(InterviewSession)
            .filter(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user.id,
            )
            .first()
        )

        if not old_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found.",
            )

        if old_session.status != "COMPLETED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only completed interviews can be retried.",
            )

        original_session_id = (
            old_session.retry_of_session_id
            or old_session.id
        )

        attempt_number = (
            self.db.query(InterviewSession)
            .filter(
                (
                    InterviewSession.id
                    == original_session_id
                )
                |
                (
                    InterviewSession.retry_of_session_id
                    == original_session_id
                )
            )
            .count()
            + 1
        )

        new_session = InterviewSession(
            user_id=user.id,
            career_recommendation_id=old_session.career_recommendation_id,
            interview_type=old_session.interview_type,
            difficulty=old_session.difficulty,
            total_questions=old_session.total_questions,
            status="ACTIVE",
            retry_of_session_id=original_session_id,
            attempt_number=attempt_number,
        )

        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)

        questions = self._generate_questions_for_session(
            new_session
        )

        return {
            "session_id": new_session.id,
            "attempt_number": new_session.attempt_number,
            "questions": questions,
        }

    def get_next_question(
        self,
        session_id: int,
    ):
        return {
            "question_number": 1,
            "question": "Explain REST API."
        }

    def submit_answer(
        self,
        session_id: int,
        data: InterviewAnswerRequest,
    ):
        """
        Submit an interview answer and evaluate it using Gemini AI.
        """

        # -----------------------------------------
        # Validate interview session
        # -----------------------------------------

        interview_session = (
            self.db.query(InterviewSession)
            .filter(
                InterviewSession.id == session_id
            )
            .first()
        )

        if not interview_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found."
            )

        # -----------------------------------------
        # Validate interview question
        # -----------------------------------------

        question = (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.id == data.question_id,
                InterviewQuestion.session_id == session_id,
            )
            .first()
        )

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview question not found."
            )

        # -----------------------------------------
        # Check whether already answered
        # -----------------------------------------

        existing_answer = (
            self.db.query(InterviewAnswer)
            .filter(
                InterviewAnswer.question_id == data.question_id
            )
            .first()
        )

        if existing_answer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question has already been answered."
            )

        # -----------------------------------------
        # Evaluate answer using Gemini
        # -----------------------------------------

        evaluation = self.answer_evaluator.evaluate(
            question=question.question,
            expected_answer=question.expected_answer,
            candidate_answer=data.answer,
        )

        # -----------------------------------------
        # Save interview answer
        # -----------------------------------------

        interview_answer = InterviewAnswer(
            question_id=question.id,
            answer=data.answer,
            technical_score=evaluation["technical_score"],
            communication_score=evaluation["communication_score"],
            confidence_score=evaluation["confidence_score"],
            overall_score=evaluation["overall_score"],
            ai_feedback=evaluation["feedback"],
        )

        self.db.add(interview_answer)

        # -----------------------------------------
        # Update interview progress
        # -----------------------------------------

        interview_session.answered_questions += 1

        self.db.commit()

        self.db.refresh(interview_session)

        # -----------------------------------------
        # Get next question
        # -----------------------------------------

        next_question = (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id == interview_session.id,
                InterviewQuestion.question_order
                == interview_session.answered_questions + 1,
            )
            .first()
        )

        # -----------------------------------------
        # Complete interview if no more questions
        # -----------------------------------------

        if next_question is None:

            interview_session.status = "COMPLETED"
            interview_session.completed_at = datetime.now(UTC)

            self.db.commit()

            self.db.refresh(interview_session)

            # -----------------------------------------
            # Generate final interview report
            # -----------------------------------------

            report_generator = ReportGenerator(self.db)

            report = report_generator.generate_report(
                interview_session.id
            )

            return {
                "message": "Interview completed successfully.",
                "answered_questions": interview_session.answered_questions,
                "total_questions": interview_session.total_questions,
                "status": interview_session.status,
                "report": report,
            }

        # -----------------------------------------
        # Return response
        # -----------------------------------------

        return {
            "message": "Answer evaluated successfully.",
            "evaluation": evaluation,
            "answered_questions": interview_session.answered_questions,
            "total_questions": interview_session.total_questions,
            "next_question": (
                {
                    "question_id": next_question.id,
                    "question": next_question.question,
                    "category": next_question.category,
                    "difficulty": next_question.difficulty,
                }
                if next_question
                else None
            ),
        }

    def finish_interview(
        self,
        session_id: int,
    ):
        return {
            "overall_score": 82,
            "total_questions": 10,
            "message": "Interview completed."
        }

    def get_history(
        self,
        user: User,
    ):
        """
        Return interview history for the logged-in user.
        """

        sessions = (
            self.db.query(InterviewSession)
            .filter(
                InterviewSession.user_id == user.id
            )
            .order_by(
                InterviewSession.created_at.desc()
            )
            .all()
        )

        history = []

        for session in sessions:
            history.append(
                {
                    "session_id": session.id,
                    "attempt_number": session.attempt_number,
                    "retry_of_session_id": session.retry_of_session_id,
                    "interview_type": session.interview_type,
                    "difficulty": session.difficulty,
                    "overall_score": session.overall_score,
                    "status": session.status,
                    "created_at": session.created_at,
                    "completed_at": session.completed_at,
                }
            )

        return history

    def get_interview_details(
        self,
        session_id: int,
        user: User,
    ):
        """
        Return complete interview details.
        """

        # -----------------------------------------
        # Validate interview session
        # -----------------------------------------

        session = (
            self.db.query(InterviewSession)
            .filter(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user.id,
            )
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found.",
            )

        # -----------------------------------------
        # Load questions
        # -----------------------------------------

        questions = (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.session_id == session.id
            )
            .order_by(
                InterviewQuestion.question_order
            )
            .all()
        )

        question_list = []

        for question in questions:

            answer = question.answer

            question_list.append(
                {
                    "question_id": question.id,
                    "question_order": question.question_order,
                    "question": question.question,
                    "category": question.category,
                    "difficulty": question.difficulty,

                    "answer": (
                        answer.answer
                        if answer
                        else None
                    ),

                    "technical_score": (
                        answer.technical_score
                        if answer
                        else None
                    ),

                    "communication_score": (
                        answer.communication_score
                        if answer
                        else None
                    ),

                    "confidence_score": (
                        answer.confidence_score
                        if answer
                        else None
                    ),

                    "overall_score": (
                        answer.overall_score
                        if answer
                        else None
                    ),

                    "ai_feedback": (
                        answer.ai_feedback
                        if answer
                        else None
                    ),
                }
            )

        # -----------------------------------------
        # Load interview report
        # -----------------------------------------

        report = (
            self.db.query(InterviewReport)
            .filter(
                InterviewReport.session_id == session.id
            )
            .first()
        )

        report_data = None

        if report:

            report_data = {
                "technical_score": report.technical_score,
                "communication_score": report.communication_score,
                "problem_solving_score": report.problem_solving_score,
                "confidence_score": report.confidence_score,
                "overall_score": report.overall_score,

                "strengths": json.loads(report.strengths)
                if report.strengths else [],

                "weaknesses": json.loads(report.weaknesses)
                if report.weaknesses else [],

                "missing_topics": json.loads(report.missing_topics)
                if report.missing_topics else [],

                "learning_resources": json.loads(report.learning_resources)
                if report.learning_resources else [],

                "suggested_projects": json.loads(report.suggested_projects)
                if report.suggested_projects else [],

                "ai_summary": report.ai_summary,

                "recommendation": (
                    json.loads(report.recommendation)
                    if report.recommendation
                    else None
                ),
            }

        # -----------------------------------------
        # Load interview feedback
        # -----------------------------------------

        feedback = None

        if report:

            feedback = (
                self.db.query(InterviewFeedback)
                .filter(
                    InterviewFeedback.report_id == report.id
                )
                .first()
            )

        feedback_data = None

        if feedback:

            feedback_data = {
                "feedback_id": feedback.id,

                "strengths": (
                    json.loads(feedback.strengths)
                    if feedback.strengths
                    else []
                ),

                "weaknesses": (
                    json.loads(feedback.weaknesses)
                    if feedback.weaknesses
                    else []
                ),

                "missing_skills": (
                    json.loads(feedback.missing_skills)
                    if feedback.missing_skills
                    else []
                ),

                "improvement_suggestions": (
                    json.loads(feedback.improvement_suggestions)
                    if feedback.improvement_suggestions
                    else []
                ),

                "learning_resources": (
                    json.loads(feedback.learning_resources)
                    if feedback.learning_resources
                    else []
                ),

                "mentor_advice": (
                    json.loads(feedback.mentor_advice)
                    if feedback.mentor_advice
                    else []
                ),
            }

        # -----------------------------------------
        # Return response
        # -----------------------------------------

        return {
            "session": {
                "session_id": session.id,
                "attempt_number": session.attempt_number,
                "retry_of_session_id": session.retry_of_session_id,
                "interview_type": session.interview_type,
                "difficulty": session.difficulty,
                "status": session.status,
                "total_questions": session.total_questions,
                "answered_questions": session.answered_questions,
                "overall_score": session.overall_score,
                "created_at": session.created_at,
                "completed_at": session.completed_at,
            },
            "questions": question_list,
            "report": report_data,
            "feedback": feedback_data,
        }

    def delete_interview(
        self,
        session_id: int,
        user: User,
    ):
        """
        Delete an interview session belonging to the logged-in user.
        """

        session = (
            self.db.query(InterviewSession)
            .filter(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user.id,
            )
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found.",
            )

        self.db.delete(session)
        self.db.commit()

        return {
            "message": "Interview deleted successfully."
        }
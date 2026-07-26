"""
Report Generator Service
Step 7.12 - Generate Final Interview Report
"""

import json
import logging

from sqlalchemy.orm import Session

from app.core.gemini import generate_content
from app.models.interview_question import InterviewQuestion
from app.models.interview_report import InterviewReport
from app.models.interview_session import InterviewSession
from app.models.interview_feedback import InterviewFeedback
from app.services.interview_scoring import InterviewScoringService

logger = logging.getLogger(__name__)


class ReportGenerator:

    def __init__(self, db: Session):
        self.db = db
        self.scoring_service = InterviewScoringService()

    def generate_report(self, session_id: int) -> dict:

        session = (
            self.db.query(InterviewSession)
            .filter(InterviewSession.id == session_id)
            .first()
        )

        if session is None:
            raise ValueError("Interview session not found.")

        questions = (
            self.db.query(InterviewQuestion)
            .filter(InterviewQuestion.session_id == session_id)
            .order_by(InterviewQuestion.question_order)
            .all()
        )

        if not questions:
            raise ValueError("Interview questions not found.")

        answers = [q.answer for q in questions if q.answer is not None]

        if not answers:
            raise ValueError("Interview answers not found.")

        technical_score = sum(a.technical_score or 0 for a in answers) / len(answers)
        communication_score = sum(a.communication_score or 0 for a in answers) / len(answers)
        confidence_score = sum(a.confidence_score or 0 for a in answers) / len(answers)

        evaluation = {
            "technical_score": technical_score,
            "practical_score": confidence_score,
            "explanation_quality": communication_score,
            "communication_score": communication_score,
            "missing_concepts": [],
        }

        score = self.scoring_service.calculate_score(evaluation)

        transcript_parts = []

        for q in questions:
            if q.answer is None:
                continue

            transcript_parts.append(
                f"""
Question:
{q.question}

Candidate Answer:
{q.answer.answer}

Technical Score:
{q.answer.technical_score}

Communication Score:
{q.answer.communication_score}

Confidence Score:
{q.answer.confidence_score}

AI Feedback:
{q.answer.ai_feedback}

----------------------------------------
"""
            )

        transcript = "\n".join(transcript_parts)

        prompt = f"""
You are an expert technical interviewer.

Analyze the interview transcript.

Overall Score:{score["final_score"]}

Technical Score:{score["technical_knowledge"]}

Interview Transcript:{transcript}

Return ONLY valid JSON.

Do not include markdown.

Do not include explanations.

Do not wrap the JSON inside triple backticks.

Every field must contain at least 3 items.

Use this exact format:

{{
    "strengths": [
        "...",
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "...",
        "..."
    ],
    "missing_topics": [
        "...",
        "...",
        "..."
    ],
    "learning_resources": [
        "...",
        "...",
        "..."
    ],
    "suggested_projects": [
        "...",
        "...",
        "..."
    ],
    "missing_skills": [
        "...",
        "...",
        "..."
    ],
    "improvement_suggestions": [
        "...",
        "...",
        "..."
    ],
    "mentor_advice": [
        "...",
        "...",
        "..."
    ]
}}
"""

        try:
            response = generate_content(prompt)

            cleaned_response = (response.text or "").strip()

            if not cleaned_response:
                raise ValueError("Gemini returned an empty response.")

            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.replace(
                    "```json", "", 1
                )

            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.replace(
                    "```", "", 1
                )

            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]

            cleaned_response = cleaned_response.strip()

            ai_result = json.loads(cleaned_response)

        except Exception:
            logger.exception("Failed to generate AI interview report")

            ai_result = {
                "strengths": [],
                "weaknesses": [],
                "missing_topics": [],
                "learning_resources": [],
                "suggested_projects": [],
                "missing_skills": [],
                "improvement_suggestions": [],
                "mentor_advice": [],
            }

        ai_result.setdefault("strengths", [])
        ai_result.setdefault("weaknesses", [])
        ai_result.setdefault("missing_topics", [])
        ai_result.setdefault("learning_resources", [])
        ai_result.setdefault("suggested_projects", [])
        ai_result.setdefault("missing_skills", [])
        ai_result.setdefault("improvement_suggestions", [])
        ai_result.setdefault("mentor_advice", [])

        report = (
            self.db.query(InterviewReport)
            .filter(
                InterviewReport.session_id == session.id
            )
            .first()
        )

        if report is None:
            report = InterviewReport(
                session_id=session.id
            )
            self.db.add(report)
            self.db.flush()

        report.technical_score = score["technical_knowledge"]
        report.communication_score = score["communication"]
        report.problem_solving_score = score["problem_solving"]
        report.confidence_score = confidence_score
        report.overall_score = score["final_score"]
        report.strengths = json.dumps(
            ai_result["strengths"]
        )
        report.weaknesses = json.dumps(
            ai_result["weaknesses"]
        )
        report.missing_topics = json.dumps(
            ai_result["missing_topics"]
        )
        report.learning_resources = json.dumps(
            ai_result["learning_resources"]
        )
        report.suggested_projects = json.dumps(
            ai_result["suggested_projects"]
        )
        
        report.ai_summary = f"""
Overall Score: {score['final_score']}

Technical Score: {score['technical_knowledge']}

Communication Score: {score['communication']}

Problem Solving Score: {score['problem_solving']}

Strengths:
{", ".join(ai_result["strengths"])}

Weaknesses:
{", ".join(ai_result["weaknesses"])}

Missing Topics:
{", ".join(ai_result["missing_topics"])}
""".strip()

        report.recommendation = json.dumps(
            {
                "missing_skills": ai_result[
                    "missing_skills"
                ],
                "learning_resources": ai_result[
                    "learning_resources"
                ],
                "suggested_projects": ai_result[
                    "suggested_projects"
                ],
            }
        )

        feedback = (
            self.db.query(InterviewFeedback)
            .filter(
                InterviewFeedback.report_id == report.id
            )
            .first()
        )

        if feedback is None:
            feedback = InterviewFeedback(
                report_id=report.id
            )
            self.db.add(feedback)

        feedback.strengths = json.dumps(
            ai_result["strengths"]
        )
        feedback.weaknesses = json.dumps(
            ai_result["weaknesses"]
        )
        feedback.missing_skills = json.dumps(
            ai_result["missing_skills"]
        )
        feedback.improvement_suggestions = json.dumps(
            ai_result["improvement_suggestions"]
        )
        feedback.learning_resources = json.dumps(
            ai_result["learning_resources"]
        )
        feedback.mentor_advice = json.dumps(
            ai_result["mentor_advice"]
        )

        session.overall_score = score["final_score"]

        try:
            self.db.commit()
            self.db.refresh(report)
            self.db.refresh(feedback)
        except Exception:
            self.db.rollback()
            raise

        return {
            "report_id": report.id,
            "session_id": report.session_id,
            "overall_score": report.overall_score,
            "technical_score": report.technical_score,
            "communication_score": report.communication_score,
            "problem_solving_score": report.problem_solving_score,
            "confidence_score": report.confidence_score,
            "strengths": ai_result["strengths"],
            "weaknesses": ai_result["weaknesses"],
            "missing_topics": ai_result["missing_topics"],
            "learning_resources": ai_result["learning_resources"],
            "suggested_projects": ai_result["suggested_projects"],
            "feedback": {
                "feedback_id": feedback.id,
                "strengths": ai_result["strengths"],
                "weaknesses": ai_result["weaknesses"],
                "missing_skills": ai_result["missing_skills"],
                "improvement_suggestions": ai_result["improvement_suggestions"],
                "learning_resources": ai_result["learning_resources"],
                "mentor_advice": ai_result["mentor_advice"],
            }
        }
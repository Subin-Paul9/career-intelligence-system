import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.gemini import (
    generate_content,
)
from app.models.interview_audio import (
    InterviewAudio,
)
from app.models.speech_transcript import (
    SpeechTranscript,
)
from app.models.interview_answer import (
    InterviewAnswer,
)
from app.models.interview_question import (
    InterviewQuestion,
)
from app.models.technical_evaluation import (
    TechnicalEvaluation,
)
from app.schemas.technical_evaluation import (
    TechnicalEvaluationResponse,
)


class TechnicalEvaluationService:
    """
    Service responsible for:

    - Loading transcript
    - Loading interview question
    - Evaluating transcript using Gemini
    - Saving evaluation
    - Returning technical evaluation
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Load Transcript
    # =====================================================

    def load_transcript(
        self,
        transcript_id: int,
    ) -> SpeechTranscript:
        """
        Load a speech transcript from the database.
        """

        transcript = (
            self.db.query(
                SpeechTranscript,
            )
            .filter(
                SpeechTranscript.id == transcript_id,
            )
            .first()
        )

        if transcript is None:
            raise HTTPException(
                status_code=404,
                detail="Speech transcript not found.",
            )

        return transcript

    # =====================================================
    # Load Interview Answer
    # =====================================================

    def load_interview_answer(
        self,
        transcript: SpeechTranscript,
    ) -> InterviewAnswer:
        """
        Load the interview answer associated
        with the transcript.
        """

        # ---------------------------------------------
        # Load Interview Audio
        # ---------------------------------------------

        interview_audio = (
            self.db.query(
                InterviewAudio,
            )
            .filter(
                InterviewAudio.id == transcript.audio_id,
            )
            .first()
        )

        if interview_audio is None:
            raise HTTPException(
                status_code=404,
                detail="Interview audio not found.",
            )

        # ---------------------------------------------
        # Load Interview Answer
        # ---------------------------------------------

        interview_answer = (
            self.db.query(
                InterviewAnswer,
            )
            .filter(
                InterviewAnswer.id
                == interview_audio.answer_id,
            )
            .first()
        )

        if interview_answer is None:
            raise HTTPException(
                status_code=404,
                detail="Interview answer not found.",
            )

        return interview_answer

    # =====================================================
    # Load Interview Question
    # =====================================================

    def load_interview_question(
        self,
        interview_answer: InterviewAnswer,
    ) -> InterviewQuestion:
        """
        Load the interview question associated
        with the interview answer.
        """

        interview_question = (
            self.db.query(
                InterviewQuestion,
            )
            .filter(
                InterviewQuestion.id
                == interview_answer.question_id,
            )
            .first()
        )

        if interview_question is None:
            raise HTTPException(
                status_code=404,
                detail="Interview question not found.",
            )

        return interview_question

    # =====================================================
    # Build Gemini Prompt
    # =====================================================

    def build_prompt(
        self,
        interview_question: InterviewQuestion,
        transcript: SpeechTranscript,
    ) -> str:
        """
        Build the Gemini prompt for evaluating
        the candidate's spoken interview answer.
        """

        return f"""
You are an expert technical interviewer.

Evaluate the candidate's spoken interview answer.

Interview Question:
{interview_question.question}

Candidate's Spoken Answer:
{transcript.transcript}

Evaluate the answer based on:

1. Technical correctness
2. Completeness
3. Accuracy
4. Depth of explanation
5. Relevance to the question

Return ONLY valid JSON in the following format.

Do not include markdown.
Do not include explanations.
Do not wrap the JSON inside ```json blocks.

{{
    "technical_score": 0,
    "strengths": [],
    "weaknesses": [],
    "improvement_suggestions": [],
    "gemini_feedback": ""
}}
"""

    # =====================================================
    # Evaluate with Gemini
    # =====================================================

    def evaluate_with_gemini(
        self,
        prompt: str,
    ) -> dict:
        """
        Send the prompt to Gemini and return
        the parsed JSON response.
        """

        try:

            response = generate_content(
                prompt,
            )

            response_text = (
                response.text
                .replace(
                    "```json",
                    "",
                )
                .replace(
                    "```",
                    "",
                )
                .strip()
            )

            return json.loads(
                response_text,
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Gemini evaluation failed: {str(e)}"
                ),
            )

    # =====================================================
    # Save Technical Evaluation
    # =====================================================

    def save_evaluation(
        self,
        transcript_id: int,
        evaluation: dict,
    ) -> TechnicalEvaluation:
        """
        Save the technical evaluation.

        If an evaluation already exists,
        update it. Otherwise, create a new one.
        """

        technical_evaluation = (
            self.db.query(
                TechnicalEvaluation,
            )
            .filter(
                TechnicalEvaluation.transcript_id
                == transcript_id,
            )
            .first()
        )

        if technical_evaluation is None:

            technical_evaluation = TechnicalEvaluation(
                transcript_id=transcript_id,
            )

            self.db.add(
                technical_evaluation,
            )

        # ---------------------------------------------
        # Update Evaluation
        # ---------------------------------------------

        technical_evaluation.technical_score = (
            evaluation["technical_score"]
        )

        technical_evaluation.strengths = (
            evaluation["strengths"]
        )

        technical_evaluation.weaknesses = (
            evaluation["weaknesses"]
        )

        technical_evaluation.improvement_suggestions = (
            evaluation["improvement_suggestions"]
        )

        technical_evaluation.gemini_feedback = (
            evaluation["gemini_feedback"]
        )

        try:

            self.db.commit()

            self.db.refresh(
                technical_evaluation,
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to save technical evaluation.",
            ) from e

        return technical_evaluation

    # =====================================================
    # Analyze Technical Evaluation
    # =====================================================

    def analyze(
        self,
        transcript_id: int,
    ) -> TechnicalEvaluationResponse:
        """
        Evaluate a spoken interview answer using Gemini.
        """

        # ---------------------------------------------
        # Load Transcript
        # ---------------------------------------------

        transcript = self.load_transcript(
            transcript_id,
        )

        # ---------------------------------------------
        # Load Interview Answer
        # ---------------------------------------------

        interview_answer = (
            self.load_interview_answer(
                transcript,
            )
        )

        # ---------------------------------------------
        # Load Interview Question
        # ---------------------------------------------

        interview_question = (
            self.load_interview_question(
                interview_answer,
            )
        )

        # ---------------------------------------------
        # Build Prompt
        # ---------------------------------------------

        prompt = self.build_prompt(
            interview_question,
            transcript,
        )

        # ---------------------------------------------
        # Evaluate Using Gemini
        # ---------------------------------------------

        evaluation = (
            self.evaluate_with_gemini(
                prompt,
            )
        )

        # ---------------------------------------------
        # Validate Gemini Response
        # ---------------------------------------------

        required_fields = [
            "technical_score",
            "strengths",
            "weaknesses",
            "improvement_suggestions",
            "gemini_feedback",
        ]

        for field in required_fields:
            if field not in evaluation:
                raise HTTPException(
                    status_code=500,
                    detail=f"Gemini response missing '{field}'.",
                )

        # ---------------------------------------------
        # Save Evaluation
        # ---------------------------------------------

        technical_evaluation = (
            self.save_evaluation(
                transcript_id=transcript.id,
                evaluation=evaluation,
            )
        )

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------

        return TechnicalEvaluationResponse(
            technical_score=technical_evaluation.technical_score,
            strengths=technical_evaluation.strengths,
            weaknesses=technical_evaluation.weaknesses,
            improvement_suggestions=technical_evaluation.improvement_suggestions,
            gemini_feedback=technical_evaluation.gemini_feedback,
            created_at=technical_evaluation.created_at,
        )
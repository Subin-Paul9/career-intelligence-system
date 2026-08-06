from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.interview_session import (
    InterviewSession,
)
from app.models.speech_transcript import (
    SpeechTranscript,
)
from app.models.technical_evaluation import (
    TechnicalEvaluation,
)
from app.models.communication_score import (
    CommunicationScore,
)
from app.models.pronunciation_analysis import (
    PronunciationAnalysis,
)
from app.models.voice_score import (
    VoiceScore,
)

from app.schemas.voice_report import (
    VoiceInterviewReportResponse,
)

from app.services.learning_resource_service import (
    LearningResourceService,
)


class VoiceReportService:
    """
    Service responsible for:

    - Loading transcript
    - Loading technical evaluation
    - Loading communication score
    - Loading pronunciation analysis
    - Loading voice score
    - Generating learning resources
    - Building the final voice interview report
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.learning_resource_service = (
            LearningResourceService()
        )

    # =====================================================
    # Load Transcript
    # =====================================================

    def load_transcript(
        self,
        transcript_id: int,
    ) -> SpeechTranscript:
        """
        Load the speech transcript associated
        with the given transcript ID.
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
    # Load Technical Evaluation
    # =====================================================

    def load_technical_evaluation(
        self,
        transcript_id: int,
    ) -> TechnicalEvaluation:
        """
        Load the technical evaluation associated
        with the transcript.
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
            raise HTTPException(
                status_code=404,
                detail="Technical evaluation not found.",
            )

        return technical_evaluation

    # =====================================================
    # Load Communication Score
    # =====================================================

    def load_communication_score(
        self,
        transcript_id: int,
    ) -> CommunicationScore:
        """
        Load the communication score associated
        with the transcript.
        """

        communication_score = (
            self.db.query(
                CommunicationScore,
            )
            .filter(
                CommunicationScore.transcript_id
                == transcript_id,
            )
            .first()
        )

        if communication_score is None:
            raise HTTPException(
                status_code=404,
                detail="Communication score not found.",
            )

        return communication_score

    # =====================================================
    # Load Pronunciation Analysis
    # =====================================================

    def load_pronunciation_analysis(
        self,
        transcript_id: int,
    ) -> PronunciationAnalysis:
        """
        Load the pronunciation analysis associated
        with the transcript.
        """

        pronunciation_analysis = (
            self.db.query(
                PronunciationAnalysis,
            )
            .filter(
                PronunciationAnalysis.transcript_id
                == transcript_id,
            )
            .first()
        )

        if pronunciation_analysis is None:
            raise HTTPException(
                status_code=404,
                detail="Pronunciation analysis not found.",
            )

        return pronunciation_analysis

    # =====================================================
    # Load Voice Score
    # =====================================================

    def load_voice_score(
        self,
        transcript_id: int,
    ) -> VoiceScore:
        """
        Load the voice score associated
        with the transcript.
        """

        voice_score = (
            self.db.query(
                VoiceScore,
            )
            .filter(
                VoiceScore.transcript_id
                == transcript_id,
            )
            .first()
        )

        if voice_score is None:
            raise HTTPException(
                status_code=404,
                detail="Voice score not found.",
            )

        return voice_score

    # =====================================================
    # Generate Voice Interview Report
    # =====================================================

    def generate_report(
        self,
        transcript_id: int,
    ) -> VoiceInterviewReportResponse:
        """
        Generate the complete voice interview report.
        """

        # ---------------------------------------------
        # Load Transcript
        # ---------------------------------------------

        transcript = (
            self.load_transcript(
                transcript_id,
            )
        )

        # ---------------------------------------------
        # Load Technical Evaluation
        # ---------------------------------------------

        technical_evaluation = (
            self.load_technical_evaluation(
                transcript_id,
            )
        )

        # ---------------------------------------------
        # Load Communication Score
        # ---------------------------------------------

        communication_score = (
            self.load_communication_score(
                transcript_id,
            )
        )

        # ---------------------------------------------
        # Load Pronunciation Analysis
        # ---------------------------------------------

        pronunciation_analysis = (
            self.load_pronunciation_analysis(
                transcript_id,
            )
        )

        # ---------------------------------------------
        # Load Voice Score
        # ---------------------------------------------

        voice_score = (
            self.load_voice_score(
                transcript_id,
            )
        )

        # ---------------------------------------------
        # Missing Concepts
        # ---------------------------------------------

        missing_concepts = list(
            technical_evaluation.weaknesses
        )

        # ---------------------------------------------
        # Learning Resources
        # ---------------------------------------------

        learning_resources = (
            self.learning_resource_service.get_learning_resources(
                missing_concepts,
            )
        )

        # ---------------------------------------------
        # Build Report
        # ---------------------------------------------

        return VoiceInterviewReportResponse(
            transcript=transcript.transcript,

            technical_score=voice_score.technical_score,

            communication_score=voice_score.communication_score,

            fluency_score=voice_score.fluency_score,

            confidence_score=voice_score.confidence_score,

            overall_score=voice_score.overall_score,

            technical_feedback=technical_evaluation.gemini_feedback,

            strengths=technical_evaluation.strengths,

            weaknesses=technical_evaluation.weaknesses,

            missing_concepts=missing_concepts,

            suggested_practice=(
                technical_evaluation.improvement_suggestions
            ),

            learning_resources=learning_resources,
        )

    # =====================================================
    # Get Report by Session
    # =====================================================

    def get_report_by_session(
        self,
        session_id: int,
    ) -> VoiceInterviewReportResponse:
        """
        Retrieve the saved voice interview report
        for an interview session.
        """

        # ---------------------------------------------
        # Load Session
        # ---------------------------------------------

        session = (
            self.db.query(
                InterviewSession,
            )
            .filter(
                InterviewSession.id == session_id,
            )
            .first()
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Interview session not found.",
            )

        # ---------------------------------------------
        # Find Transcript
        # ---------------------------------------------

        transcript_id = None

        for question in session.questions:

            if question.answer is None:
                continue

            if question.answer.audio is None:
                continue

            if question.answer.audio.transcript is None:
                continue

            transcript_id = (
                question.answer.audio.transcript.id
            )

            break

        if transcript_id is None:
            raise HTTPException(
                status_code=404,
                detail="Voice interview report not found.",
            )

        # ---------------------------------------------
        # Generate Report
        # ---------------------------------------------

        return self.generate_report(
            transcript_id=transcript_id,
        )
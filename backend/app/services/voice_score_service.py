from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.communication_score import (
    CommunicationScore,
)
from app.models.pronunciation_analysis import (
    PronunciationAnalysis,
)
from app.models.technical_evaluation import (
    TechnicalEvaluation,
)
from app.models.voice_score import (
    VoiceScore,
)
from app.schemas.voice_score import (
    VoiceScoreResponse,
)


class VoiceScoreService:
    """
    Service responsible for:

    - Loading technical evaluation
    - Loading communication score
    - Loading pronunciation analysis
    - Calculating overall voice score
    - Saving score
    - Returning voice score
    """

    TECHNICAL_WEIGHT = 0.60
    COMMUNICATION_WEIGHT = 0.25
    FLUENCY_WEIGHT = 0.10
    CONFIDENCE_WEIGHT = 0.05

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

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
    # Calculate Overall Voice Score
    # =====================================================

    def calculate_overall_score(
        self,
        technical_evaluation: TechnicalEvaluation,
        communication_score: CommunicationScore,
        pronunciation_analysis: PronunciationAnalysis,
    ) -> float:
        """
        Calculate the weighted overall voice score.

        Weights:

        - Technical Score      : 60%
        - Communication Score  : 25%
        - Fluency Score        : 10%
        - Confidence Score     : 5%
        """

        for score in [
            technical_evaluation.technical_score,
            communication_score.overall_score,
            communication_score.fluency_score,
            pronunciation_analysis.speech_confidence,
        ]:
            if not 0 <= score <= 100:
                raise HTTPException(
                    status_code=500,
                    detail="Invalid score value.",
                )

        technical = (
            technical_evaluation.technical_score
        )

        communication = (
            communication_score.overall_score
        )

        fluency = (
            communication_score.fluency_score
        )

        confidence = (
            pronunciation_analysis.speech_confidence
        )

        overall_score = (
            (technical * self.TECHNICAL_WEIGHT)
            + (communication * self.COMMUNICATION_WEIGHT)
            + (fluency * self.FLUENCY_WEIGHT)
            + (confidence * self.CONFIDENCE_WEIGHT)
        )

        return round(
            overall_score,
            2,
        )

    # =====================================================
    # Save Voice Score
    # =====================================================

    def save_score(
        self,
        transcript_id: int,
        technical_evaluation: TechnicalEvaluation,
        communication_score: CommunicationScore,
        pronunciation_analysis: PronunciationAnalysis,
        overall_score: float,
    ) -> VoiceScore:
        """
        Save the calculated voice score.

        If a score already exists,
        update it. Otherwise, create a new one.
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

            voice_score = VoiceScore(
                transcript_id=transcript_id,
            )

            self.db.add(
                voice_score,
            )

        # ---------------------------------------------
        # Update Scores
        # ---------------------------------------------

        voice_score.technical_score = (
            technical_evaluation.technical_score
        )

        voice_score.communication_score = (
            communication_score.overall_score
        )

        voice_score.fluency_score = (
            communication_score.fluency_score
        )

        voice_score.confidence_score = (
            pronunciation_analysis.speech_confidence
        )

        voice_score.overall_score = (
            overall_score
        )

        try:

            self.db.commit()

            self.db.refresh(
                voice_score,
            )

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to save voice score.",
            ) from e

        return voice_score

    # =====================================================
    # Calculate Voice Score
    # =====================================================

    def calculate(
        self,
        transcript_id: int,
    ) -> VoiceScoreResponse:
        """
        Calculate the final voice interview score.
        """

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
        # Calculate Overall Score
        # ---------------------------------------------

        overall_score = (
            self.calculate_overall_score(
                technical_evaluation,
                communication_score,
                pronunciation_analysis,
            )
        )

        # ---------------------------------------------
        # Save Voice Score
        # ---------------------------------------------

        voice_score = (
            self.save_score(
                transcript_id=transcript_id,
                technical_evaluation=technical_evaluation,
                communication_score=communication_score,
                pronunciation_analysis=pronunciation_analysis,
                overall_score=overall_score,
            )
        )

        # ---------------------------------------------
        # Return Response
        # ---------------------------------------------

        return VoiceScoreResponse(
            technical_score=voice_score.technical_score,
            communication_score=voice_score.communication_score,
            fluency_score=voice_score.fluency_score,
            confidence_score=voice_score.confidence_score,
            overall_score=voice_score.overall_score,
            created_at=voice_score.created_at,
        )
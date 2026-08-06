from sqlalchemy.orm import Session

from app.models.user import User

from app.services.voice_session_service import (
    VoiceSessionService,
)

from app.services.speech_to_text_service import (
    SpeechToTextService,
)

from app.services.voice_analysis_service import (
    VoiceAnalysisService,
)

from app.services.technical_evaluation_service import (
    TechnicalEvaluationService,
)

from app.services.communication_analysis_service import (
    CommunicationAnalysisService,
)

from app.services.filler_word_detection_service import (
    FillerWordDetectionService,
)

from app.services.pronunciation_analysis_service import (
    PronunciationAnalysisService,
)

from app.services.voice_score_service import (
    VoiceScoreService,
)

from app.services.voice_report_service import (
    VoiceReportService,
)


class VoiceInterviewService:
    """
    Master service responsible for executing the
    complete voice interview analysis pipeline.

    Pipeline:

    1. Create Voice Interview Session
    2. Generate Transcript
    3. Analyze voice metrics
    4. Technical evaluation
    5. Communication analysis
    6. Filler word detection
    7. Pronunciation analysis
    8. Calculate voice score
    9. Complete interview session
    10. Generate final report
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.voice_session_service = (
            VoiceSessionService(db)
        )

        self.speech_service = (
            SpeechToTextService(db)
        )

        self.voice_analysis_service = (
            VoiceAnalysisService(db)
        )

        self.technical_service = (
            TechnicalEvaluationService(db)
        )

        self.communication_service = (
            CommunicationAnalysisService(db)
        )

        self.filler_word_service = (
            FillerWordDetectionService(db)
        )

        self.pronunciation_service = (
            PronunciationAnalysisService(db)
        )

        self.voice_score_service = (
            VoiceScoreService(db)
        )

        self.report_service = (
            VoiceReportService(db)
        )

    # =====================================================
    # Analyze Voice Interview
    # =====================================================

    def analyze(
        self,
        user: User,
        audio_id: int,
    ):
        """
        Execute the complete voice interview
        analysis pipeline.
        """

        # ---------------------------------------------
        # Create Voice Interview Session
        # ---------------------------------------------

        voice_session = (
            self.voice_session_service.create_session(
                user=user,
            )
        )

        # ---------------------------------------------
        # Generate Transcript
        # ---------------------------------------------

        transcript = (
            self.speech_service.generate_transcript(
                audio_id=audio_id,
            )
        )

        # ---------------------------------------------
        # Voice Analysis
        # ---------------------------------------------

        voice_analysis = (
            self.voice_analysis_service.analyze(
                audio_id=audio_id,
            )
        )

        # ---------------------------------------------
        # Technical Evaluation
        # ---------------------------------------------

        technical_evaluation = (
            self.technical_service.analyze(
                transcript_id=transcript.transcript_id,
            )
        )

        # ---------------------------------------------
        # Communication Analysis
        # ---------------------------------------------

        communication_score = (
            self.communication_service.analyze(
                transcript_id=transcript.transcript_id,
            )
        )

        # ---------------------------------------------
        # Filler Word Detection
        # ---------------------------------------------

        filler_word_analysis = (
            self.filler_word_service.analyze(
                transcript_id=transcript.transcript_id,
            )
        )

        # ---------------------------------------------
        # Pronunciation Analysis
        # ---------------------------------------------

        pronunciation_analysis = (
            self.pronunciation_service.analyze(
                transcript_id=transcript.transcript_id,
            )
        )

        # ---------------------------------------------
        # Voice Score
        # ---------------------------------------------

        voice_score = (
            self.voice_score_service.calculate(
                transcript_id=transcript.transcript_id,
            )
        )

        # ---------------------------------------------
        # Complete Voice Interview Session
        # ---------------------------------------------

        self.voice_session_service.complete_session(
            session=voice_session,
            overall_score=voice_score.overall_score,
        )

        # ---------------------------------------------
        # Generate Final Report
        # ---------------------------------------------

        report = (
            self.report_service.generate_report(
                transcript_id=transcript.transcript_id,
            )
        )

        # ---------------------------------------------
        # Return Report
        # ---------------------------------------------

        return report
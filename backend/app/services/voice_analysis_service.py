from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydub import AudioSegment
from pydub.silence import detect_silence

from app.models.interview_audio import InterviewAudio
from app.models.speech_transcript import SpeechTranscript
from app.models.voice_analysis import VoiceAnalysis
from app.schemas.voice_interview import VoiceAnalysisResponse


class VoiceAnalysisService:
    """
    Service responsible for:

    - Loading interview audio
    - Detecting speech and silence
    - Calculating voice metrics
    - Saving analysis results
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Load Interview Audio
    # =====================================================

    def load_audio(
        self,
        audio_id: int,
    ) -> InterviewAudio:
        """
        Load an interview audio record.
        """

        audio = (
            self.db.query(InterviewAudio)
            .filter(
                InterviewAudio.id == audio_id
            )
            .first()
        )

        if audio is None:
            raise HTTPException(
                status_code=404,
                detail="Interview audio not found.",
            )

        audio_path = Path(audio.file_path)

        if not audio_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Audio file not found on disk.",
            )

        return audio

    # =====================================================
    # Load Audio Segment
    # =====================================================

    def load_audio_segment(
        self,
        audio: InterviewAudio,
    ) -> AudioSegment:
        """
        Load the audio waveform using pydub.
        """

        try:

            audio_segment = AudioSegment.from_file(
                audio.file_path,
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail="Failed to load audio file.",
            ) from e

        return audio_segment

    # =====================================================
    # Detect Silence Regions
    # =====================================================

    def detect_silence_regions(
        self,
        audio_segment: AudioSegment,
    ) -> list[list[int]]:
        """
        Detect silent regions in the audio.

        Returns:
            List of silence intervals in milliseconds.

        Example:
            [
                [1200, 1850],
                [5300, 6100],
                [9800, 10450],
            ]
        """

        try:
            silence_threshold = (
                audio_segment.dBFS - 16
                if audio_segment.dBFS != float("-inf")
                else -50
            )

            silence_regions = detect_silence(
                audio_segment,
                min_silence_len=500,
                silence_thresh=silence_threshold,
            )

        except Exception as e:

            raise HTTPException(
                status_code=500,
                detail="Failed to detect silence regions.",
            ) from e

        return silence_regions

    # =====================================================
    # Calculate Silence Duration
    # =====================================================

    def calculate_silence_duration(
        self,
        silence_regions: list[list[int]],
    ) -> float:
        """
        Calculate the total silence duration.

        Args:
            silence_regions:
                List of silence intervals in milliseconds.

        Returns:
            Total silence duration in seconds.
        """

        total_silence_ms = sum(
            end - start
            for start, end in silence_regions
        )

        total_silence_seconds = (
            total_silence_ms / 1000
        )

        return round(
            total_silence_seconds,
            2,
        )

    # =====================================================
    # Calculate Speech Duration
    # =====================================================

    def calculate_speech_duration(
        self,
        audio_segment: AudioSegment,
        silence_duration: float,
    ) -> float:
        """
        Calculate the total speaking duration.

        Args:
            audio_segment:
                Loaded audio.

            silence_duration:
                Total silence duration in seconds.

        Returns:
            Speech duration in seconds.
        """

        total_duration = (
            len(audio_segment) / 1000
        )

        speech_duration = (
            total_duration - silence_duration
        )

        return round(
            max(
                speech_duration,
                0.0,
            ),
            2,
        )

    # =====================================================
    # Calculate Pause Count
    # =====================================================

    def calculate_pause_count(
        self,
        silence_regions: list[list[int]],
    ) -> int:
        """
        Calculate the total number of pauses.

        Args:
            silence_regions:
                List of silence intervals.

        Returns:
            Number of pauses.
        """

        return len(silence_regions)

    # =====================================================
    # Calculate Long Pause Count
    # =====================================================

    def calculate_long_pause_count(
        self,
        silence_regions: list[list[int]],
    ) -> int:
        """
        Count the number of long pauses.

        A long pause is defined as any silence
        lasting 2 seconds or longer.

        Args:
            silence_regions:
                List of silence intervals in milliseconds.

        Returns:
            Number of long pauses.
        """

        LONG_PAUSE_THRESHOLD = 2000  # milliseconds

        long_pause_count = sum(
            1
            for start, end in silence_regions
            if (end - start) >= LONG_PAUSE_THRESHOLD
        )

        return long_pause_count

    # =====================================================
    # Calculate Average Pause
    # =====================================================

    def calculate_average_pause(
        self,
        silence_regions: list[list[int]],
    ) -> float:
        """
        Calculate the average pause duration.

        Args:
            silence_regions:
                List of silence intervals in milliseconds.

        Returns:
            Average pause duration in seconds.
        """

        if not silence_regions:
            return 0.0

        total_pause_ms = sum(
            end - start
            for start, end in silence_regions
        )

        average_pause = (
            total_pause_ms
            / len(silence_regions)
            / 1000
        )

        return round(
            average_pause,
            2,
        )

    # =====================================================
    # Calculate Longest Pause
    # =====================================================

    def calculate_longest_pause(
        self,
        silence_regions: list[list[int]],
    ) -> float:
        """
        Calculate the longest pause duration.

        Args:
            silence_regions:
                List of silence intervals in milliseconds.

        Returns:
            Longest pause duration in seconds.
        """

        if not silence_regions:
            return 0.0

        longest_pause_ms = max(
            end - start
            for start, end in silence_regions
        )

        longest_pause = (
            longest_pause_ms / 1000
        )

        return round(
            longest_pause,
            2,
        )

    # =====================================================
    # Calculate Speaking Consistency
    # =====================================================

    def calculate_speaking_consistency(
        self,
        silence_regions: list[list[int]],
    ) -> float:
        """
        Calculate speaking consistency based on
        pause duration variation.

        Returns:
            Consistency score between 0 and 100.
        """

        if len(silence_regions) <= 1:
            return 100.0

        pause_durations = [
            (end - start) / 1000
            for start, end in silence_regions
        ]

        average_pause = (
            sum(pause_durations)
            / len(pause_durations)
        )

        if average_pause == 0:
            return 100.0

        average_deviation = (
            sum(
                abs(
                    pause - average_pause
                )
                for pause in pause_durations
            )
            / len(pause_durations)
        )

        consistency = max(
            0.0,
            100.0
            - (
                average_deviation
                / average_pause
            )
            * 100,
        )

        return round(
            consistency,
            2,
        )

    # =====================================================
    # Calculate Words Per Minute
    # =====================================================

    def calculate_words_per_minute(
        self,
        audio_id: int,
        speech_duration: float,
    ) -> float:
        """
        Calculate the speaking rate (Words Per Minute).

        Args:
            audio_id:
                Interview audio ID.

            speech_duration:
                Speaking duration in seconds.

        Returns:
            Words per minute.
        """

        if speech_duration <= 0:
            return 0.0

        transcript = (
            self.db.query(SpeechTranscript)
            .filter(
                SpeechTranscript.audio_id == audio_id
            )
            .first()
        )

        if transcript is None:
            raise HTTPException(
                status_code=404,
                detail="Speech transcript not found.",
            )

        word_count = len(
            (transcript.transcript or "").split()
        )

        words_per_minute = (
            word_count * 60
        ) / speech_duration

        return round(
            words_per_minute,
            2,
        )

    # =====================================================
    # Save Voice Analysis
    # =====================================================

    def save_analysis(
        self,
        audio_id: int,
        speech_duration: float,
        silence_duration: float,
        words_per_minute: float,
        pause_count: int,
        long_pause_count: int,
        average_pause: float,
        longest_pause: float,
        speaking_consistency: float,
    ) -> VoiceAnalysis:
        """
        Save the calculated voice analysis.

        If an analysis already exists, update it.
        Otherwise, create a new one.
        """

        analysis = (
            self.db.query(VoiceAnalysis)
            .filter(
                VoiceAnalysis.audio_id == audio_id
            )
            .first()
        )

        if analysis is None:

            analysis = VoiceAnalysis(
                audio_id=audio_id,
            )

            self.db.add(analysis)

        # ---------------------------------------------
        # Update Metrics
        # ---------------------------------------------

        analysis.speech_duration = (
            speech_duration
        )

        analysis.silence_duration = (
            silence_duration
        )

        analysis.words_per_minute = (
            words_per_minute
        )

        analysis.pause_count = (
            pause_count
        )

        analysis.long_pause_count = (
            long_pause_count
        )

        analysis.average_pause = (
            average_pause
        )

        analysis.longest_pause = (
            longest_pause
        )

        analysis.speaking_consistency = (
            speaking_consistency
        )

        try:

            self.db.commit()

            self.db.refresh(analysis)

        except Exception as e:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Failed to save voice analysis.",
            ) from e

        return analysis

    # =====================================================
    # Analyze Voice
    # =====================================================

    def analyze(
        self,
        audio_id: int,
    ) -> VoiceAnalysisResponse:
        """
        Perform complete voice analysis for an
        interview audio recording.
        """

        # -------------------------------------------------
        # Load Audio
        # -------------------------------------------------

        audio = self.load_audio(
            audio_id=audio_id,
        )

        # -------------------------------------------------
        # Load Audio Segment
        # -------------------------------------------------

        audio_segment = self.load_audio_segment(
            audio,
        )

        # -------------------------------------------------
        # Detect Silence
        # -------------------------------------------------

        silence_regions = self.detect_silence_regions(
            audio_segment,
        )

        # -------------------------------------------------
        # Calculate Metrics
        # -------------------------------------------------

        silence_duration = (
            self.calculate_silence_duration(
                silence_regions,
            )
        )

        speech_duration = (
            self.calculate_speech_duration(
                audio_segment,
                silence_duration,
            )
        )

        pause_count = (
            self.calculate_pause_count(
                silence_regions,
            )
        )

        long_pause_count = (
            self.calculate_long_pause_count(
                silence_regions,
            )
        )

        average_pause = (
            self.calculate_average_pause(
                silence_regions,
            )
        )

        longest_pause = (
            self.calculate_longest_pause(
                silence_regions,
            )
        )

        speaking_consistency = (
            self.calculate_speaking_consistency(
                silence_regions,
            )
        )

        words_per_minute = (
            self.calculate_words_per_minute(
                audio_id=audio.id,
                speech_duration=speech_duration,
            )
        )

        # -------------------------------------------------
        # Save Analysis
        # -------------------------------------------------

        analysis = self.save_analysis(
            audio_id=audio.id,
            speech_duration=speech_duration,
            silence_duration=silence_duration,
            words_per_minute=words_per_minute,
            pause_count=pause_count,
            long_pause_count=long_pause_count,
            average_pause=average_pause,
            longest_pause=longest_pause,
            speaking_consistency=speaking_consistency,
        )

        # -------------------------------------------------
        # Return Response
        # -------------------------------------------------

        return VoiceAnalysisResponse(
            speech_duration=analysis.speech_duration,
            silence_duration=analysis.silence_duration,
            words_per_minute=analysis.words_per_minute,
            pause_count=analysis.pause_count,
            long_pause_count=analysis.long_pause_count,
            average_pause=analysis.average_pause,
            longest_pause=analysis.longest_pause,
            speaking_consistency=analysis.speaking_consistency,
            created_at=analysis.created_at,
        )
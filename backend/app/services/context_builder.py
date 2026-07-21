from sqlalchemy.orm import Session

from app.models.user import User
from app.models.resume import Resume
from app.models.recommendation import Recommendation

from app.services.project_recommendation_service import (
    ProjectRecommendationService,
)
from app.services.certification_recommendation_service import (
    CertificationRecommendationService,
)
from app.services.learning_recommendation_service import (
    LearningRecommendationService,
)
from app.services.roadmap_generator_service import (
    RoadmapGeneratorService,
)
from app.services.career_recommendation_comparison_service import (
    CareerRecommendationComparisonService,
)


class ContextBuilder:
    """
    Builds the context used by the AI Assistant.
    """

    def __init__(self, db: Session):
        self.db = db

    def build_context(self, user_id: int) -> dict:
        """
        Build a complete AI context for a user.
        """

        # -------------------------
        # User Profile
        # -------------------------
        user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        profile: dict = {
            "name": None,
            "email": None,
            "role": None,
        }

        if user:
            profile = {
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "role": user.role,
            }

        # -------------------------
        # Latest Resume
        # -------------------------
        resume = (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
            .first()
        )

        resume_data: dict = {
            "file_name": None,
            "resume_text": None,
        }

        ats_score = None
        resume_suggestions = None

        if resume:
            resume_data = {
                "file_name": resume.file_name,
                "resume_text": resume.resume_text,
            }

            ats_score = resume.ats_score
            resume_suggestions = resume.feedback

        # -------------------------
        # Latest Recommendation
        # -------------------------
        recommendation = (
            self.db.query(Recommendation)
            .filter(Recommendation.user_id == user_id)
            .order_by(Recommendation.generated_at.desc())
            .first()
        )

        career = None
        match_score = None
        missing_skills: list[str] = []

        if recommendation:
            career = recommendation.career
            match_score = recommendation.match_score

            if recommendation.missing_skills:
                missing_skills = [
                    skill.strip()
                    for skill in recommendation.missing_skills.split(",")
                    if skill.strip()
                ]

        # -------------------------
        # Learning Resources
        # -------------------------
        learning_service = LearningRecommendationService()

        resources = learning_service.recommend_resources(
            missing_skills=missing_skills,
        )

        # -------------------------
        # Recommended Projects
        # -------------------------
        project_service = ProjectRecommendationService()

        projects = project_service.recommend_projects(
            career=career,
            missing_skills=missing_skills,
        )

        # -------------------------
        # Recommended Certifications
        # -------------------------
        certification_service = (
            CertificationRecommendationService()
        )

        certifications = (
            certification_service.recommend_certifications(
                career=career,
                missing_skills=missing_skills,
            )
        )

        # -------------------------
        # Personalized Roadmap
        # -------------------------
        roadmap_service = RoadmapGeneratorService()

        resume_text = (
            resume_data.get(
                "resume_text",
                "",
            ).lower()
        )

        known_skills = [
            "Python",
            "Java",
            "C",
            "C++",
            "JavaScript",
            "TypeScript",
            "HTML",
            "CSS",
            "React",
            "Next.js",
            "FastAPI",
            "Django",
            "Flask",
            "SQL",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Docker",
            "Git",
            "GitHub",
            "REST API",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "NumPy",
            "Pandas",
            "Linux",
            "Cloud",
            "AWS",
            "Azure",
            "Cybersecurity",
            "Networking",
        ]

        current_skills = [
            skill
            for skill in known_skills
            if skill.lower() in resume_text
        ]

        roadmap = roadmap_service.generate_roadmap(
            career=career,
            missing_skills=missing_skills,
            current_skills=current_skills,
        )

        # -------------------------
        # Career Comparison
        # -------------------------
        comparison_service = (
            CareerRecommendationComparisonService()
        )

        career_comparison = (
            comparison_service.compare(
                career=career,
                match_score=match_score,
            )
        )

        # -------------------------
        # Return Context
        # -------------------------
        return {
            "profile": profile,
            "resume": resume_data,
            "ats_score": ats_score,
            "resume_suggestions": resume_suggestions,
            "career": career,
            "match_score": match_score,
            "missing_skills": missing_skills,
            "resources": resources,
            "projects": projects,
            "certifications": certifications,
            "roadmap": roadmap,
            "career_comparison": career_comparison,
        }
from app.prompts.general_prompt import GENERAL_TEMPLATE
from app.prompts.resume_prompt import RESUME_TEMPLATE
from app.prompts.ats_prompt import ATS_TEMPLATE
from app.prompts.career_prompt import CAREER_TEMPLATE
from app.prompts.project_prompt import PROJECT_TEMPLATE
from app.prompts.certification_prompt import CERTIFICATION_TEMPLATE
from app.prompts.learning_prompt import LEARNING_TEMPLATE
from app.prompts.roadmap_prompt import ROADMAP_TEMPLATE
from app.prompts.comparison_prompt import COMPARISON_TEMPLATE
from app.prompts.interview_prompt import INTERVIEW_TEMPLATE


class PromptRouter:
    """
    Selects the most appropriate prompt template
    based on the user's question.
    """

    @staticmethod
    def get_template(question: str) -> str:
        question = question.lower().strip()

        # Resume
        if any(keyword in question for keyword in [
            "resume",
            "cv",
        ]):
            return RESUME_TEMPLATE

        # ATS
        if any(keyword in question for keyword in [
            "ats",
            "keyword",
            "keywords",
        ]):
            return ATS_TEMPLATE

        # Projects
        if any(keyword in question for keyword in [
            "project",
            "portfolio",
        ]):
            return PROJECT_TEMPLATE

        # Certifications
        if any(keyword in question for keyword in [
            "certification",
            "certifications",
            "certificate",
            "certificates",
        ]):
            return CERTIFICATION_TEMPLATE

        # Roadmap
        if any(keyword in question for keyword in [
            "roadmap",
            "plan",
            "learning path",
        ]):
            return ROADMAP_TEMPLATE

        # Career Comparison
        if any(keyword in question for keyword in [
            "compare",
            "comparison",
            "difference",
            "vs",
            "versus",
        ]):
            return COMPARISON_TEMPLATE

        # Interview
        if any(keyword in question for keyword in [
            "interview",
            "behavioral",
            "technical interview",
        ]):
            return INTERVIEW_TEMPLATE

        # Career Guidance
        if any(keyword in question for keyword in [
            "career",
            "job",
            "role",
        ]):
            return CAREER_TEMPLATE

        # Learning Resources
        if any(keyword in question for keyword in [
            "learn",
            "study",
            "resource",
            "resources",
            "course",
            "courses",
        ]):
            return LEARNING_TEMPLATE

        # Default
        return GENERAL_TEMPLATE
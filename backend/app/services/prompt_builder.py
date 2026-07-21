from app.services.prompt_router import PromptRouter


class PromptBuilder:
    """
    Builds a structured prompt for the Gemini AI model.
    """

    @staticmethod
    def build_prompt(
        context: dict,
        question: str,
    ) -> str:
        """
        Generate a structured prompt using the user's context
        and current question.
        """

        profile = context.get("profile", {})
        resume = context.get("resume", {})
        resources = context.get("resources", [])
        projects = context.get("projects", [])
        certifications = context.get("certifications", [])
        roadmap = context.get("roadmap")
        career_comparison = context.get("career_comparison")

        # Select the appropriate prompt template
        template = PromptRouter.get_template(question)

        # Resume Preview
        resume_text = resume.get("resume_text") or ""
        resume_preview = (
            resume_text[:2000] + "..."
            if len(resume_text) > 2000
            else resume_text
        )

        # Missing Skills
        missing_skills = "\n".join(
            f"- {skill}"
            for skill in context.get(
                "missing_skills",
                [],
            )
        ) or "None"

        # Learning Resources
        resource_text = "\n".join(
            (
                f"- {r.get('skill', 'Unknown Skill')}: "
                f"{r.get('resource', 'No Resource Available')}"
            )
            for r in resources
        ) or "None"

        # Recommended Projects
        project_text = "\n\n".join(
            (
                f"Title: {p.get('title', 'Not Available')}\n"
                f"Difficulty: {p.get('difficulty', 'Not Available')}\n"
                f"Description: {p.get('description', 'Not Available')}\n"
                f"Skills: "
                f"{', '.join(p.get('skills', []))}\n"
                f"Matched Skills: "
                f"{', '.join(p.get('matched_skills', []))}"
            )
            for p in projects
        ) or "None"

        # Recommended Certifications
        certification_text = "\n\n".join(
            (
                f"Name: {c.get('name', 'Not Available')}\n"
                f"Provider: {c.get('provider', 'Not Available')}\n"
                f"Difficulty: {c.get('difficulty', 'Not Available')}\n"
                f"Description: {c.get('description', 'Not Available')}\n"
                f"Skills: "
                f"{', '.join(c.get('skills', []))}\n"
                f"Matched Skills: "
                f"{', '.join(c.get('matched_skills', []))}\n"
                f"Official URL: "
                f"{c.get('url', 'Not Available')}"
            )
            for c in certifications
        ) or "None"

        # Career Roadmap
        roadmap_text = ""

        if roadmap:
            day30 = "\n".join(
                f"- {item}"
                for item in roadmap.get(
                    "day_30",
                    [],
                )
            ) or "None"

            day60 = "\n".join(
                f"- {item}"
                for item in roadmap.get(
                    "day_60",
                    [],
                )
            ) or "None"

            day90 = "\n".join(
                f"- {item}"
                for item in roadmap.get(
                    "day_90",
                    [],
                )
            ) or "None"

            roadmap_text = f"""
## CAREER ROADMAP

Career:
{roadmap.get("career", "Not Available")}

30-Day Plan:
{day30}

60-Day Plan:
{day60}

90-Day Plan:
{day90}
"""

        # Career Comparison
        comparison_text = ""

        if career_comparison:
            c1 = career_comparison.get(
                "career_1",
                {},
            )

            c2 = career_comparison.get(
                "career_2",
                {},
            )

            comparison_text = f"""
## CAREER COMPARISON

Career 1:
{c1.get("name", "Not Available")}

Salary:
{c1.get("salary", "Not Available")}

Demand:
{c1.get("demand", "Not Available")}

Growth:
{c1.get("growth", "Not Available")}

Skills:
{", ".join(c1.get("skills", [])) or "None"}

Roadmap:
{" → ".join(c1.get("roadmap", [])) or "None"}

----------------------------------------

Career 2:
{c2.get("name", "Not Available")}

Salary:
{c2.get("salary", "Not Available")}

Demand:
{c2.get("demand", "Not Available")}

Growth:
{c2.get("growth", "Not Available")}

Skills:
{", ".join(c2.get("skills", [])) or "None"}

Roadmap:
{" → ".join(c2.get("roadmap", [])) or "None"}
"""

        # Properly dedented prompt block
        prompt = f"""
{template}

Use the context below to answer the user's question.

## USER PROFILE

Student Name:
{profile.get("name") or "Not Available"}

Email:
{profile.get("email") or "Not Available"}

Role:
{profile.get("role") or "Not Available"}

## RESUME

File Name:
{resume.get("file_name") or "Not Available"}

Resume Text:
{resume_preview or "Not Available"}

ATS Score:
{context.get("ats_score") or "Not Available"}

Resume Suggestions:
{context.get("resume_suggestions") or "Not Available"}

## CAREER RECOMMENDATION

Recommended Career:
{context.get("career") or "Not Available"}

Match Score:
{context.get("match_score") or "Not Available"}

Missing Skills:
{missing_skills}

Learning Resources:
{resource_text}

## RECOMMENDED PROJECTS

{project_text}

## RECOMMENDED CERTIFICATIONS

{certification_text}

{roadmap_text}

{comparison_text}

## USER QUESTION

{question}

## RESPONSE INSTRUCTIONS

- Base your answer only on the provided context.
- Use the selected prompt template to guide your response.
- Recommend projects only from the provided recommended projects list.
- Recommend certifications only from the provided recommended certifications list.
- Recommend learning resources only from the provided learning resources.
- Use the personalized roadmap whenever relevant.
- Use career comparison only when comparison information is available.
- If information is unavailable, clearly state that.
- Do not invent facts, careers, projects, certifications, resources, or roadmap steps.

Return ONLY valid JSON using exactly this format:

{{
    "answer": "Provide a detailed, helpful, and professional response here.",
    "career": "Recommended career name or null",
    "resources": [
        "Resource 1",
        "Resource 2"
    ]
}}

Rules:
- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT wrap the JSON in triple backticks.
- The "answer" field must always be a string.
- The "career" field must be a string or null.
- The "resources" field must always be an array of strings.
"""

        return prompt.strip()
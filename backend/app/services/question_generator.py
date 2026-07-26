"""
Question Generator Service

This service is responsible for:

- Building Gemini prompts
- Generating interview questions
- Parsing AI responses
- Validating generated questions
"""

import json
from typing import Any

from app.core.gemini import generate_content

Question = dict[str, Any]
QuestionList = list[Question]


class QuestionGenerator:
    """
    Generates personalized interview questions
    using Gemini AI.
    """

    def __init__(self):
        pass

    def _build_prompt(
        self,
        context: dict,
        number_of_questions: int,
    ) -> str:
        """
        Build the prompt for Gemini AI to generate
        personalized interview questions.
        """

        prompt = f"""
You are an experienced technical interviewer.

Generate {number_of_questions} personalized interview questions for the candidate.

IMPORTANT:
Return EXACTLY {number_of_questions} questions.
Do not generate more or fewer questions.

Candidate Information
---------------------
Career:
{context["career"]}

Difficulty:
{context["difficulty"]}

ATS Score:
{context["ats_score"]}

Previous Interview Score:
{context["previous_interview_score"]}

Candidate Skills:
{", ".join(context["skills"])}

Missing Skills:
{", ".join(context["missing_skills"])}

Resume Feedback:
{context["resume_feedback"]}

Resume:
{context["resume_text"]}

Requirements
------------
Generate a balanced interview containing:

- Technical Questions
- Behavioral Questions
- HR Questions
- Scenario-Based Questions
- Problem-Solving Questions

The questions should:

- Match the candidate's career.
- Match the selected difficulty.
- Focus on candidate strengths.
- Test missing skills.
- Include resume/project-based questions.
- Increase difficulty gradually.

Question Distribution:

Generate exactly {number_of_questions} questions.

Distribute the questions as naturally as possible among:

- Technical
- Scenario-Based
- Behavioral
- HR
- Problem-Solving

The distribution should depend on the requested number of questions while ensuring a balanced interview.

Return ONLY valid JSON.

Format:

[
    {{
        "question": "...",
        "category": "Technical",
        "difficulty": "{context["difficulty"]}",
        "expected_answer": "A concise model answer describing the key concepts expected from the candidate."
    }}
]

Rules:

- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT wrap the JSON inside ```json.
- Do NOT include explanations.
- Do NOT include numbering.
- Do NOT include additional text.
- Every question MUST include an "expected_answer".
- The expected_answer should:
    - Be technically correct.
    - Be concise (maximum 150 words).
    - Cover the important points expected from the candidate.
"""

        return prompt

    def _parse_response(
        self,
        response_text: str,
    ) -> QuestionList:
        """
        Parse Gemini response into a list of interview questions.
        """

        response_text = response_text.strip()

        if response_text.startswith("```json"):
            response_text = response_text.replace(
                "```json",
                "",
                1,
            )

        if response_text.startswith("```"):
            response_text = response_text.replace(
                "```",
                "",
                1,
            )

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        try:
            return json.loads(response_text)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned an invalid JSON response."
            ) from exc

    def _validate_questions(
        self,
        questions: QuestionList,
        expected_count: int,
    ) -> QuestionList:
        """
        Validate the AI-generated interview questions.
        """

        if not isinstance(questions, list):
            raise ValueError(
                "Gemini response must be a list of questions."
            )

        allowed_categories = {
            "Technical",
            "Behavioral",
            "HR",
            "Scenario-Based",
            "Problem-Solving",
        }

        validated_questions = []

        for question in questions:

            if not isinstance(question, dict):
                continue

            question_text = question.get(
                "question",
                "",
            ).strip()

            category = question.get(
                "category",
                "",
            ).strip()

            difficulty = question.get(
                "difficulty",
                "",
            ).strip()

            expected_answer = question.get(
                "expected_answer",
                "",
            ).strip()

            if not question_text:
                continue

            if category not in allowed_categories:
                continue

            if not difficulty:
                continue

            if not expected_answer:
                continue

            validated_questions.append(
                {
                    "question": question_text,
                    "category": category,
                    "difficulty": difficulty,
                    "expected_answer": expected_answer,
                }
            )

        if len(validated_questions) < expected_count:
            raise ValueError(
                f"Expected at least {expected_count} questions "
                f"but received "
                f"{len(validated_questions)} valid questions."
            )

        # If Gemini returns extra questions, keep only the requested number.
        return validated_questions[:expected_count]

    def generate_questions(
        self,
        context: dict,
        number_of_questions: int = 10,
    ) -> QuestionList:
        """
        Generate, parse, and validate interview questions.

        Returns:
            List of validated interview question dictionaries.
        """

        prompt = self._build_prompt(
            context=context,
            number_of_questions=number_of_questions,
        )

        response = generate_content(prompt)

        # Your existing generate_content() helper returns a string,
        # so pass it directly to the parser.
        questions = self._parse_response(
            response.text
        )

        validated_questions = self._validate_questions(
            questions=questions,
            expected_count=number_of_questions,
        )

        return validated_questions
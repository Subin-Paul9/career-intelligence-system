from sqlalchemy import exists
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.gemini import generate_content
from app.models.assistant_feedback import AssistantFeedback
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.schemas.ai_assistant import AIChatResponse
from app.services.context_builder import ContextBuilder
from app.services.prompt_builder import PromptBuilder
from app.services.response_formatter import ResponseFormatter
from app.services.career_comparison_service import (
    CareerComparisonService,
)
from app.services.roadmap_generator_service import (
    RoadmapGeneratorService,
)
from app.services.prompt_injection_filter import PromptInjectionFilter


class AIAssistantService:
    """
    Service responsible for handling AI assistant conversations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(
        self,
        user_id: int,
        title: str,
    ) -> Conversation:
        """
        Create a new conversation for the user.
        """
        
        conversation = Conversation(
            user_id=user_id,
            title=title.strip(),
        )
        
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation

    def get_conversations(
        self,
        user_id: int,
    ) -> list[Conversation]:
        """
        Return all conversations
        belonging to the user.
        """

        return (
            self.db.query(Conversation)
            .filter(
                Conversation.user_id == user_id,
            )
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

    def get_chat_history(
        self,
        user_id: int,
        conversation_id: int,
    ) -> list[ChatHistory]:
        """
        Return chat history for a conversation.
        """

        conversation = (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

        return (
            self.db.query(ChatHistory)
            .filter(
                ChatHistory.conversation_id == conversation_id,
            )
            .order_by(
                ChatHistory.created_at.asc()
            )
            .all()
        )

    def delete_conversation(
        self,
        user_id: int,
        conversation_id: int,
    ) -> None:
        """
        Delete a conversation belonging to the user.
        """

        conversation = (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

        self.db.delete(conversation)
        self.db.commit()

    def submit_feedback(
        self,
        user_id: int,
        chat_id: int,
        rating: int,
        comment: str | None,
    ) -> dict:
        """
        Save user feedback for an assistant response.
        """

        # -------------------------
        # Validate Chat
        # -------------------------
        chat = (
            self.db.query(ChatHistory)
            .join(Conversation)
            .filter(
                ChatHistory.id == chat_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if chat is None:
            raise HTTPException(
                status_code=404,
                detail="Chat not found.",
            )

        # -------------------------
        # Prevent Duplicate Feedback
        # -------------------------
        already_exists = (
            self.db.query(
                exists().where(
                    AssistantFeedback.chat_id == chat_id
                )
            )
            .scalar()
        )

        if already_exists:
            raise HTTPException(
                status_code=400,
                detail="Feedback already submitted.",
            )

        # -------------------------
        # Save Feedback
        # -------------------------
        feedback = AssistantFeedback(
            chat_id=chat_id,
            rating=rating,
            comment=comment,
        )

        self.db.add(feedback)
        self.db.commit()

        return {
            "message": "Feedback submitted successfully."
        }

    def chat(
        self,
        user_id: int,
        conversation_id: int,
        message: str,
    ) -> AIChatResponse:
        """
        Process a user's message and return the AI response.
        """

        # -------------------------
        # Validate Conversation
        # -------------------------
        conversation = (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

        # Save the user's message
        self.save_chat(
            conversation_id=conversation_id,
            role="user",
            message=message,
        )

        ai_result = self.generate_answer(
            user_id=user_id,
            message=message,
        )

        # Save only the assistant's answer
        self.save_chat(
            conversation_id=conversation_id,
            role="assistant",
            message=ai_result["answer"],
            prompt_tokens=ai_result["prompt_tokens"],
            response_tokens=ai_result["response_tokens"],
        )

        return AIChatResponse(
            conversation_id=conversation_id,
            answer=ai_result["answer"],
            career=ai_result["career"],
            resources=ai_result["resources"],
            prompt_tokens=ai_result["prompt_tokens"],
            response_tokens=ai_result["response_tokens"],
        )

    def generate_answer(
        self,
        user_id: int,
        message: str,
    ) -> dict:
        """
        Generate an AI response using the user's context.
        """

        # Validate user input
        PromptInjectionFilter.validate(message)

        # -------------------------
        # Build User Context
        # -------------------------
        context = ContextBuilder(
            self.db,
        ).build_context(user_id)

        # -------------------------
        # Career Comparison
        # -------------------------
        comparison_service = (
            CareerComparisonService()
        )

        career_comparison = None

        careers = (
            comparison_service.extract_careers(
                message
            )
        )

        if len(careers) >= 2:
            career_comparison = (
                comparison_service.compare_careers(
                    careers[0],
                    careers[1],
                )
            )

        context["career_comparison"] = (
            career_comparison
        )

        # -------------------------
        # Roadmap Generator
        # -------------------------
        roadmap_service = (
            RoadmapGeneratorService()
        )

        resume = context.get(
            "resume",
            {},
        )

        resume_text = (
            resume.get(
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

        roadmap = (
            roadmap_service.generate_roadmap(
                career=context.get("career"),
                missing_skills=context.get(
                    "missing_skills",
                    [],
                ),
                current_skills=current_skills,
            )
        )

        context["roadmap"] = roadmap

        # -------------------------
        # Build Prompt
        # -------------------------
        prompt = PromptBuilder.build_prompt(
            context=context,
            question=message,
        )

        return self.call_gemini(prompt)

    def call_gemini(
        self,
        prompt: str,
    ) -> dict:
        """
        Send the prompt to Gemini and return the formatted response.
        """

        try:
            response = generate_content(prompt)

        except Exception as e:
            error = str(e)
            
            if "429" in error:
                raise HTTPException(
                    status_code=429,
                    detail=(
                        "Gemini API quota exceeded. "
                        "Please try again later."
                    ),
                )
            
            raise HTTPException(
                status_code=500,
                detail=f"Gemini API Error: {error}",
            )

        prompt_tokens = 0
        response_tokens = 0

        usage = getattr(
            response,
            "usage_metadata",
            None,
        )

        if usage:
            prompt_tokens = (
                getattr(
                    usage,
                    "prompt_token_count",
                    0,
                )
                or 0
            )

            response_tokens = (
                getattr(
                    usage,
                    "candidates_token_count",
                    0,
                )
                or 0
            )

        formatted_response = (
            ResponseFormatter.format_response(
                response.text or ""
            )
        )

        return {
            "answer": formatted_response["answer"],
            "career": formatted_response["career"],
            "resources": formatted_response["resources"],
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
        }

    def save_chat(
        self,
        conversation_id: int,
        role: str,
        message: str,
        prompt_tokens: int = 0,
        response_tokens: int = 0,
    ) -> ChatHistory:
        """
        Save a chat message to the database.
        """

        chat = ChatHistory(
            conversation_id=conversation_id,
            role=role,
            message=message,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat
    
    def get_projects(
        self,
        user_id: int,
    ) -> list[dict]:
        """
        Return personalized project recommendations.
        """

        context = ContextBuilder(
            self.db
        ).build_context(user_id)

        return context.get("projects", [])
    
    def get_certifications(
        self,
        user_id: int,
    ) -> list[dict]:
        """
        Get certification recommendations for the user.
        """

        context = ContextBuilder(
            self.db
        ).build_context(user_id)

        return context.get(
            "certifications",
            [],
        )
    
    def get_resources(
        self,
        user_id: int,
    ) -> list[dict]:
        """
        Get personalized learning resources for the user.
        """

        context = ContextBuilder(
            self.db
        ).build_context(user_id)

        return context.get(
            "resources",
            [],
        )

    def get_roadmap(
        self,
        user_id: int,
    ) -> dict:
        """
        Return personalized career roadmap.
        """

        context = ContextBuilder(
            self.db
        ).build_context(user_id)

        return context.get(
            "roadmap",
            {},
        )
    
    def get_career_comparison(
        self,
        user_id: int,
    ) -> dict:
        """
        Return career comparison for the
        user's recommended career.
        """

        context = ContextBuilder(
            self.db
        ).build_context(user_id)

        return context.get(
            "career_comparison",
            {},
        )
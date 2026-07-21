from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.rate_limiter import limiter
from app.database.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User

from app.data.question_catalog import COMMON_QUESTIONS

from app.schemas.assistant import (
    QuestionsResponse,
    ProjectsResponse,
    CertificationsResponse,
    ResourcesResponse,
    RoadmapResponse,
    CareerComparisonResponse,
)

from app.schemas.ai_assistant import (
    AIChatRequest,
    AIChatResponse,
    ConversationCreateRequest,
    ConversationResponse,
    ConversationsResponse,
    HistoryResponse,
    FeedbackRequest,
    FeedbackResponse,
)

from app.services.ai_assistant_service import (
    AIAssistantService,
)

router = APIRouter(
    prefix="/api/assistant",
    tags=["AI Assistant"],
)


@router.post(
    "/conversations",
    response_model=ConversationResponse,
)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationResponse:
    """
    Create a new AI assistant conversation.
    """

    assistant = AIAssistantService(db)

    conversation = assistant.create_conversation(
        user_id=current_user.id,
        title=request.title,
    )

    return ConversationResponse.model_validate(
        conversation
    )


@router.get(
    "/conversations",
    response_model=ConversationsResponse,
)
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationsResponse:
    """
    Return all conversations for the logged-in user.
    """

    assistant = AIAssistantService(db)

    conversations = assistant.get_conversations(
        current_user.id,
    )

    return ConversationsResponse(
        conversations=conversations,
    )


@router.get(
    "/history/{conversation_id}",
    response_model=HistoryResponse,
)
def get_chat_history(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HistoryResponse:
    """
    Return chat history for a conversation.
    """

    assistant = AIAssistantService(db)

    history = assistant.get_chat_history(
        user_id=current_user.id,
        conversation_id=conversation_id,
    )

    return HistoryResponse(
        history=history,
    )


@router.delete(
    "/conversations/{conversation_id}",
    status_code=204,
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a conversation.
    """

    assistant = AIAssistantService(db)

    assistant.delete_conversation(
        user_id=current_user.id,
        conversation_id=conversation_id,
    )


@router.post(
    "/chat",
    response_model=AIChatResponse,
)
@limiter.limit("20/minute")
def chat(
    request: Request,
    chat_request: AIChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AIChatResponse:
    """
    Send a message to the AI Assistant.
    """

    assistant = AIAssistantService(db)

    return assistant.chat(
        user_id=current_user.id,
        conversation_id=chat_request.conversation_id,
        message=chat_request.message,
    )


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
)
def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FeedbackResponse:
    """
    Submit feedback for an AI assistant response.
    """

    assistant = AIAssistantService(db)

    result = assistant.submit_feedback(
        user_id=current_user.id,
        chat_id=request.chat_id,
        rating=request.rating,
        comment=request.comment,
    )

    return FeedbackResponse(
        **result,
    )


@router.get(
    "/questions",
    response_model=QuestionsResponse,
)
def get_common_questions() -> QuestionsResponse:
    """
    Return common AI assistant questions.
    """
    return QuestionsResponse(
        questions=COMMON_QUESTIONS
    )


@router.get(
    "/projects",
    response_model=ProjectsResponse,
)
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectsResponse:
    """
    Return personalized project recommendations.
    """

    assistant = AIAssistantService(db)

    projects = assistant.get_projects(
        current_user.id
    )

    return ProjectsResponse(
        projects=projects
    )


@router.get(
    "/certifications",
    response_model=CertificationsResponse,
)
def get_certifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CertificationsResponse:
    """
    Return personalized certification recommendations.
    """

    assistant = AIAssistantService(db)

    certifications = assistant.get_certifications(
        current_user.id
    )

    return CertificationsResponse(
        certifications=certifications
    )


@router.get(
    "/resources",
    response_model=ResourcesResponse,
)
def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResourcesResponse:
    """
    Return personalized learning resources.
    """

    assistant = AIAssistantService(db)

    resources = assistant.get_resources(
        current_user.id
    )

    return ResourcesResponse(
        resources=resources
    )


@router.get(
    "/roadmap",
    response_model=RoadmapResponse,
)
def get_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RoadmapResponse:
    """
    Return personalized career roadmap.
    """

    assistant = AIAssistantService(db)

    roadmap = assistant.get_roadmap(
        current_user.id
    )

    return RoadmapResponse(
        **roadmap
    )


@router.get(
    "/compare-careers",
    response_model=CareerComparisonResponse,
)
def get_career_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CareerComparisonResponse:
    """
    Return career comparison based on the user's
    recommended career.
    """

    assistant = AIAssistantService(db)

    comparison = assistant.get_career_comparison(
        current_user.id
    )

    return CareerComparisonResponse(
        **comparison
    )
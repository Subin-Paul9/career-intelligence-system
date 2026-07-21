from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AIChatRequest(BaseModel):
    conversation_id: int
    message: str


class AIChatResponse(BaseModel):
    conversation_id: int
    answer: str
    career: str | None = None
    resources: list[str] = Field(default_factory=list)
    prompt_tokens: int
    response_tokens: int


class ConversationCreateRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ConversationsResponse(BaseModel):
    conversations: list[ConversationResponse] = Field(
        default_factory=list
    )


class ChatHistoryResponse(BaseModel):
    id: int
    role: str
    message: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class HistoryResponse(BaseModel):
    history: list[ChatHistoryResponse] = Field(
        default_factory=list
    )


class FeedbackRequest(BaseModel):
    chat_id: int

    rating: int = Field(
        ge=1,
        le=5,
    )

    comment: str | None = Field(
        default=None,
        max_length=1000,
    )


class FeedbackResponse(BaseModel):
    message: str


class SuggestedQuestionsResponse(BaseModel):
    questions: list[str] = Field(
        default_factory=list
    )
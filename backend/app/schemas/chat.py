from typing import Literal

from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    session_id: str | None = None
    user_id: str
    message: str


class ChatMessageResponse(BaseModel):
    session_id: str
    response: str


class ChatSessionResponse(BaseModel):
    session_id: str
    greeting: str


class WebSocketGreeting(BaseModel):
    type: Literal["greeting"]
    session_id: str
    response: str


class WebSocketMessage(BaseModel):
    type: Literal["message"]
    session_id: str
    response: str

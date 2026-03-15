from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSessionResponse,
    WebSocketGreeting,
    WebSocketMessage,
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api/chat", tags=["Chat"])
chat_service = ChatService()


@router.post("/session", response_model=ChatSessionResponse)
async def create_session(user_id: str) -> ChatSessionResponse:
    """Create a new chat session with injected user context.

    Args:
        user_id: The unique identifier of the user.

    Returns:
        ChatSessionResponse with session_id and greeting message.

    Raises:
        HTTPException: If session creation fails.
    """
    try:
        session_id, greeting = await chat_service.create_session_with_greeting(user_id)
        return ChatSessionResponse(session_id=session_id, greeting=greeting)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(request: ChatMessageRequest) -> ChatMessageResponse:
    """Send a message to the agent.

    Automatically creates a session if it doesn't exist.

    Args:
        request: ChatMessageRequest with user_id, message, and optional session_id.

    Returns:
        ChatMessageResponse with session_id and agent response.

    Raises:
        HTTPException: If message processing fails.
    """
    try:
        if request.session_id is None:
            session_id = await chat_service.create_session(request.user_id)
        else:
            session_id = request.session_id

        response = await chat_service.send_message(
            session_id=session_id,
            user_id=request.user_id,
            message=request.message,
        )
        return ChatMessageResponse(session_id=session_id, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str) -> None:
    """WebSocket endpoint for real-time chat.

    Maintains a persistent connection for bidirectional messaging with the agent.

    Args:
        websocket: The WebSocket connection.
        user_id: The unique identifier of the user.
    """
    await websocket.accept()

    try:
        session_id, greeting = await chat_service.create_session_with_greeting(user_id)
        await websocket.send_json(
            WebSocketGreeting(type="greeting", session_id=session_id, response=greeting).model_dump()
        )

        while True:
            message = await websocket.receive_text()
            response = await chat_service.send_message(
                session_id=session_id,
                user_id=user_id,
                message=message,
            )
            await websocket.send_json(
                WebSocketMessage(type="message", session_id=session_id, response=response).model_dump()
            )
    except WebSocketDisconnect:
        pass

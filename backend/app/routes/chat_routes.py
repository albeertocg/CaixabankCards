import logging

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect

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
logger = logging.getLogger(__name__)


@router.post("/session", response_model=ChatSessionResponse)
async def create_session(user_id: str) -> ChatSessionResponse:
    try:
        session_id, greeting = await chat_service.create_session_with_greeting(user_id)
        return ChatSessionResponse(session_id=session_id, greeting=greeting)
    except Exception:
        logger.exception("Error al crear sesion de chat")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(request: ChatMessageRequest) -> ChatMessageResponse:
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
    except Exception:
        logger.exception("Error al procesar mensaje de chat")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/history/{session_id}")
async def get_history(session_id: str):
    try:
        messages = await chat_service.get_history(session_id)
        return {"session_id": session_id, "messages": messages}
    except Exception:
        logger.exception("Error al obtener historial de chat")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.websocket("/ws/{user_id}")
async def websocket_chat(
    websocket: WebSocket,
    user_id: str,
    session_id: str = Query(default=None),
) -> None:
    await websocket.accept()

    try:
        sid, greeting = await chat_service.create_session_with_greeting(user_id)
        history = await chat_service.get_history(sid) if session_id else []

        await websocket.send_json(
            WebSocketGreeting(
                type="greeting",
                session_id=sid,
                response=greeting,
            ).model_dump()
        )

        if history:
            for msg in history:
                await websocket.send_json(
                    {
                        "type": "history",
                        "role": msg["role"],
                        "text": msg["text"],
                    }
                )

        await _websocket_message_loop(websocket, sid, user_id)
    except WebSocketDisconnect:
        pass


async def _websocket_message_loop(
    websocket: WebSocket,
    session_id: str,
    user_id: str,
) -> None:
    while True:
        message = await websocket.receive_text()
        response = await chat_service.send_message(
            session_id=session_id,
            user_id=user_id,
            message=message,
        )
        await websocket.send_json(
            WebSocketMessage(
                type="message",
                session_id=session_id,
                response=response,
            ).model_dump()
        )

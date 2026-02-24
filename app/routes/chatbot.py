"""
Rutas para el chatbot
"""
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.chatbot_service import chatbot_service

router = APIRouter(prefix="/chat", tags=["Chatbot"])


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Envía un mensaje al chatbot y recibe una respuesta
    
    Args:
        request: Objeto con el mensaje del usuario
        
    Returns:
        ChatResponse con la respuesta del chatbot
        
    Raises:
        HTTPException: Si hay error en la comunicación con el modelo
    """
    try:
        response_text = await chatbot_service.get_response(request.message)
        return ChatResponse(response=response_text, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

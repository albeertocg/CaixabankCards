"""
Modelo de Chat para la interacción con el chatbot
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Modelo para la pregunta del usuario"""
    message: str = Field(..., description="Pregunta o mensaje del usuario", min_length=1)


class ChatResponse(BaseModel):
    """Modelo para la respuesta del chatbot"""
    response: str = Field(..., description="Respuesta del chatbot")
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")

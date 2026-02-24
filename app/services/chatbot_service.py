"""
Servicio para gestionar la interacción con el chatbot de Gemini
"""
import os
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class ChatbotService:
    """Servicio para gestionar las conversaciones con Gemini"""

    def __init__(self):
        """Inicializa el servicio de chatbot"""
        api_key = os.getenv("API_GEMINI_KEY")
        if not api_key:
            raise ValueError("API_GEMINI_KEY no está configurada en las variables de entorno")
        
        self.client = genai.Client(api_key=api_key)

    async def get_response(self, message: str) -> str:
        """
        Obtiene una respuesta del modelo de Gemini
        
        Args:
            message: Pregunta o mensaje del usuario
            
        Returns:
            Respuesta generada por el modelo
            
        Raises:
            Exception: Si hay error en la comunicación con la API
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=message
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error al comunicarse con Gemini: {str(e)}")


# Instancia singleton del servicio
chatbot_service = ChatbotService()

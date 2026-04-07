"""Chat service orchestrating session creation with context and message handling."""

from google.genai import types
from app.config.settings import settings
from app.agent.agent import runner, session_service
from app.agent.context import build_user_context
from app.services.guardrail_service import GuardrailService

class ChatService:
    """Service for managing chat sessions and message exchanges with the card recommendation agent."""
    
    def __init__(self) -> None:
            self.guardrail_service = GuardrailService()
            
            
    async def create_session(self, user_id: str) -> str:
        """Create a chat session and inject user context.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The created session ID.
        """
        context = await build_user_context(user_id)

        session = await session_service.create_session(
            app_name="caixabank_card_advisor",
            user_id=user_id,
        )

        # Inyectar contexto como primer mensaje para que el agente lo procese
        context_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"[CONTEXTO DEL CLIENTE]\n{context}\n\n"
                    "Saluda brevemente al cliente por su nombre y pregúntale en qué puedes ayudarle."
                )
            ],
        )

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=context_message,
        ):
            pass  # Agent processes context silently

        return session.id

    async def create_session_with_greeting(self, user_id: str) -> tuple[str, str]:
        """Create session with context and return greeting.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            Tuple of (session_id, greeting_message).
        """
        context = await build_user_context(user_id)

        session = await session_service.create_session(
            app_name="caixabank_card_advisor",
            user_id=user_id,
        )

        context_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"[CONTEXTO DEL CLIENTE]\n{context}\n\n"
                    "Saluda brevemente al cliente por su nombre y pregúntale en qué puedes ayudarle."
                )
            ],
        )

        greeting = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=context_message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                greeting = event.content.parts[0].text

        return session.id, greeting

    async def send_message(self, session_id: str, user_id: str, message: str) -> str:
        """Send user message and return agent response.

        Args:
            session_id: The session ID for this conversation.
            user_id: The unique identifier of the user.
            message: The user's message text.

        Returns:
            The agent's response text.
        """
        print(f"[CHAT] mensaje usuario: {message!r}")
        guardrail_result = self.guardrail_service.validate(message)
        print(f"[CHAT] guardrail allowed={guardrail_result.allowed} response={guardrail_result.response!r}")

        if not guardrail_result.allowed:
            return guardrail_result.response

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)],
        )

        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text

        return response_text

import logging

from google.genai import types
from app.config.settings import settings
from app.agent.agent import runner, session_service
from app.agent.context import build_user_context
from app.repositories.chat_repository import ChatRepository
from app.services.guardrail_service import GuardrailService
from app.services.sanitizer import sanitize_text, contains_injection

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self) -> None:
        self.guardrail_service = GuardrailService()
        self.chat_repo = ChatRepository()

    async def _get_or_create_session(
        self,
        user_id: str,
    ) -> tuple[str, str]:
        existing = await self.chat_repo.find_active_session(user_id)
        if existing:
            session_id = existing["session_id"]
            adk_session = await session_service.get_session(
                app_name="caixabank_card_advisor",
                user_id=user_id,
                session_id=session_id,
            )
            if adk_session is not None:
                return session_id, existing.get("greeting", "")

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

        await self.chat_repo.deactivate_sessions(user_id)
        await self.chat_repo.create_session(session.id, user_id, greeting)

        return session.id, greeting

    async def create_session(self, user_id: str) -> str:
        session_id, _ = await self._get_or_create_session(user_id)
        return session_id

    async def create_session_with_greeting(self, user_id: str) -> tuple[str, str]:
        return await self._get_or_create_session(user_id)

    async def send_message(self, session_id: str, user_id: str, message: str) -> str:
        logger.debug("Mensaje usuario: %s", message)

        if contains_injection(message):
            logger.warning("Prompt injection detectado: %s", message[:100])
            return (
                "Solo puedo ayudarte con consultas relacionadas con tarjetas CaixaBank. "
                "Puedo explicarte beneficios, comisiones, requisitos o recomendarte una tarjeta."
            )

        clean_message = sanitize_text(message)
        guardrail_result = self.guardrail_service.validate(
            clean_message,
            is_followup=True,
        )
        logger.debug(
            "Guardrail allowed=%s response=%s",
            guardrail_result.allowed,
            guardrail_result.response,
        )

        if not guardrail_result.allowed:
            return guardrail_result.response

        await self.chat_repo.save_message(session_id, user_id, "user", clean_message)

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=clean_message)],
        )

        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text

        await self.chat_repo.save_message(
            session_id, user_id, "assistant", response_text
        )

        return response_text

    async def get_history(self, session_id: str) -> list[dict]:
        return await self.chat_repo.get_messages(session_id)

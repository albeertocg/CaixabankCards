"""B – Context injection and profile tests."""

import pytest

from app.tests.conftest import set_active_user, VIAJERO, SIN_TRANSACCIONES_ALTO
from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService


@pytest.mark.asyncio
class TestContextInjection:
    async def test_b1_greeting_mentions_user_name(self, chat: ChatService):
        set_active_user(VIAJERO)
        _, greeting = await chat.create_session_with_greeting("test_user_fixture")

        assert_criteria(
            response=greeting,
            criteria=[
                {
                    "name": "saludo_personalizado",
                    "instruction": "La respuesta menciona al usuario por su nombre (Carlos).",
                },
                {
                    "name": "en_español",
                    "instruction": "La respuesta está completamente en español.",
                },
            ],
            context="Usuario: Carlos Viajes Test. Viajero frecuente con 55k€ de ingresos.",
        )

    async def test_b2_no_transactions_profile_based(
        self, session_sin_tx_alto, chat: ChatService
    ):
        response = await chat.send_message(
            session_sin_tx_alto["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "basado_en_perfil",
                    "instruction": (
                        "Sin historial de transacciones, la recomendación se basa en "
                        "datos del perfil (ingresos, edad, situación laboral)."
                    ),
                },
                {
                    "name": "recomienda_tarjeta",
                    "instruction": "Recomienda al menos una tarjeta concreta por nombre.",
                },
            ],
            context="Pedro Premium Test, 80k€ ingresos, 45 años, SIN transacciones.",
        )

    async def test_b3_user_not_found(self, chat: ChatService):
        set_active_user(None)
        _, greeting = await chat.create_session_with_greeting("nonexistent_user")

        assert_criteria(
            response=greeting,
            criteria=[
                {
                    "name": "respuesta_coherente",
                    "instruction": (
                        "Sin datos de usuario, el agente responde de forma coherente. "
                        "No crashea ni devuelve errores técnicos."
                    ),
                },
            ],
            context="El usuario no existe en la base de datos.",
        )

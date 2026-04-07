"""E – Category switch mid-conversation tests."""

import pytest

from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService


@pytest.mark.asyncio
class TestCategorySwitch:
    async def test_e1_switch_viajes_to_compras(
        self, session_viajero, chat: ChatService
    ):
        await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta de viajes me recomiendas?",
        )

        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Y para compras online? ¿Cuál me iría mejor?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "nueva_categoria",
                    "instruction": (
                        "La recomendación ahora es de compras online "
                        "(E-Commerce Basic, Advanced o Premium), no de viajes."
                    ),
                },
                {
                    "name": "no_repite_anterior",
                    "instruction": (
                        "No repite la misma recomendación de viajes anterior. "
                        "Adapta la respuesta a la nueva categoría."
                    ),
                },
            ],
            context="Carlos pidió primero viajes, ahora cambia a compras online.",
        )

    async def test_e2_return_to_original_category(
        self, session_viajero, chat: ChatService
    ):
        await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta de viajes me recomiendas?",
        )

        await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Y para compras online?",
        )

        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "Mejor volvamos a viajes, ¿cuál era la mejor opción?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "vuelve_a_viajes",
                    "instruction": (
                        "Vuelve a recomendar una tarjeta de viajes "
                        "(Travel Classic, Gold o Platinum)."
                    ),
                },
            ],
            context="Carlos vuelve a preguntar por viajes tras pasar por compras online.",
        )

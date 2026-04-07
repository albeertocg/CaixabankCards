"""G – Edge case tests."""

import pytest

from app.tests.conftest import set_active_user, VIAJERO
from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService


@pytest.mark.asyncio
class TestEdgeCases:
    async def test_g1_no_matching_category(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Tenéis alguna tarjeta especial para gastos de mascotas?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "no_inventa_categoria",
                    "instruction": (
                        "No inventa una tarjeta o categoría de mascotas inexistente. "
                        "Las categorías reales son: viajes, compras online, "
                        "supermercado, restaurante/ocio y clásica."
                    ),
                },
                {
                    "name": "redirige_o_explica",
                    "instruction": (
                        "Redirige al usuario hacia las categorías disponibles "
                        "o sugiere la más cercana a su necesidad."
                    ),
                },
            ],
            context="Carlos pregunta por una categoría que no existe en el catálogo.",
        )

    async def test_g2_nonexistent_card_name(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Soy elegible para la CaixaBank Diamante?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "tarjeta_no_existe",
                    "instruction": (
                        "Indica que la tarjeta 'CaixaBank Diamante' no existe "
                        "o no está en el catálogo."
                    ),
                },
                {
                    "name": "sugiere_reales",
                    "instruction": "Sugiere tarjetas reales del catálogo CaixaBank.",
                },
            ],
            context="Carlos pregunta por una tarjeta que no existe.",
        )

    async def test_g3_followup_without_context(
        self, session_viajero, chat: ChatService
    ):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Cuánto cuesta?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "maneja_ambiguedad",
                    "instruction": (
                        "Ante una pregunta ambigua ('¿Cuánto cuesta?') sin tarjeta "
                        "especificada, el agente pide aclaración o responde en base "
                        "al contexto de la conversación. No inventa una tarjeta al azar."
                    ),
                },
            ],
            context="Carlos pregunta '¿Cuánto cuesta?' sin especificar tarjeta.",
        )

    async def test_g4_multiple_questions_one_message(
        self, session_viajero, chat: ChatService
    ):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Cuál me recomiendas para viajes y cuál para supermercado?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "aborda_viajes",
                    "instruction": "Responde sobre tarjetas de viajes.",
                },
                {
                    "name": "aborda_supermercado",
                    "instruction": "Responde sobre tarjetas de supermercado.",
                },
            ],
            context="Carlos hace dos preguntas en un solo mensaje: viajes y supermercado.",
        )

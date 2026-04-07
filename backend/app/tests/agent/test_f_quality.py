"""F – Response quality tests."""

import pytest

from app.agent.data.card_registry import CARD_REGISTRY
from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService


CARD_NAMES = {card.nombre for card in CARD_REGISTRY}


@pytest.mark.asyncio
class TestResponseQuality:
    async def test_f1_complete_structure(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "nombre_tarjeta",
                    "instruction": "Menciona al menos una tarjeta CaixaBank concreta por nombre.",
                },
                {
                    "name": "beneficios",
                    "instruction": "Explica beneficios de la tarjeta recomendada.",
                },
                {
                    "name": "comisiones",
                    "instruction": "Menciona costes o comisiones.",
                },
                {
                    "name": "requisitos",
                    "instruction": "Indica requisitos de la tarjeta.",
                },
                {
                    "name": "alternativa",
                    "instruction": "Ofrece al menos una alternativa.",
                },
            ],
            context="Carlos, viajero frecuente, 55k€.",
        )

    async def test_f2_real_data_not_hallucinated(
        self, session_viajero, chat: ChatService
    ):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "Dame los detalles de la CaixaBank Travel Gold: cashback, cuota y límite.",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "cashback_correcto",
                    "instruction": (
                        "El cashback de la Travel Gold es 1.5%. "
                        "Verifica que la respuesta menciona 1.5% o un valor coherente, "
                        "no un dato inventado."
                    ),
                },
                {
                    "name": "cuota_correcta",
                    "instruction": (
                        "La cuota anual de la Travel Gold es 50€. "
                        "Verifica que menciona 50€ o un valor similar, no inventado."
                    ),
                },
                {
                    "name": "limite_correcto",
                    "instruction": (
                        "El límite de crédito de la Travel Gold es 12.000€. "
                        "Verifica que menciona 12.000€ o un valor similar."
                    ),
                },
            ],
            context="Travel Gold real: cashback 1.5%, cuota 50€, límite 12.000€.",
        )

    async def test_f3_always_spanish(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "What credit card do you recommend for traveling?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "respuesta_en_español",
                    "instruction": (
                        "Aunque la pregunta está en inglés, la respuesta "
                        "está completamente en español."
                    ),
                },
            ],
            context="Pregunta en inglés. El agente debe responder siempre en español.",
        )

    async def test_f4_always_offers_alternative(
        self, session_shopper, chat: ChatService
    ):
        response = await chat.send_message(
            session_shopper["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas para compras online?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "tiene_alternativa",
                    "instruction": (
                        "La respuesta incluye al menos una tarjeta alternativa "
                        "además de la principal recomendada."
                    ),
                },
            ],
            context="Laura, compradora online, 32k€.",
        )

    async def test_f5_no_internal_details_exposed(
        self, session_viajero, chat: ChatService
    ):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "sin_detalles_tecnicos",
                    "instruction": (
                        "La respuesta NO menciona nombres de herramientas internas "
                        "(search_similar_cards, retrieve_card_documentation, "
                        "check_card_eligibility), ni 'system prompt', ni 'tool call', "
                        "ni nombres de funciones Python."
                    ),
                },
            ],
            context="Verificar que no se filtran detalles internos del agente.",
        )

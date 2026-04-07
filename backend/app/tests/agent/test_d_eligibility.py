"""D – Eligibility and alternatives tests."""

import pytest

from app.tests.conftest import set_active_user, NO_ELEGIBLE_PREMIUM, MENOR_EDAD, VIAJERO
from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService


@pytest.mark.asyncio
class TestEligibility:
    async def test_d1_not_eligible_for_premium(
        self, session_no_elegible, chat: ChatService
    ):
        response = await chat.send_message(
            session_no_elegible["session_id"],
            "test_user_fixture",
            "Quiero la CaixaBank Travel Platinum, ¿puedo solicitarla?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "indica_no_elegible",
                    "instruction": (
                        "Indica que el usuario NO cumple los requisitos para "
                        "la Travel Platinum (necesita 60k€, tiene 20k€)."
                    ),
                },
                {
                    "name": "ofrece_alternativa_inferior",
                    "instruction": (
                        "Sugiere una alternativa de tier inferior "
                        "(Travel Classic o Travel Gold) para la que sí sea elegible."
                    ),
                },
                {
                    "name": "en_español",
                    "instruction": "Toda la respuesta está en español.",
                },
            ],
            context="Javier, 20k€ ingresos, 30 años. Pide Travel Platinum (requiere 60k€).",
        )

    async def test_d2_underage_user(self, chat: ChatService):
        set_active_user(MENOR_EDAD)
        session_id, _ = await chat.create_session_with_greeting("test_user_fixture")

        response = await chat.send_message(
            session_id,
            "test_user_fixture",
            "¿Puedo solicitar alguna tarjeta de CaixaBank?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "restriccion_edad",
                    "instruction": (
                        "Indica que el usuario de 16 años no cumple la edad mínima "
                        "requerida para las tarjetas (mínimo 18 años)."
                    ),
                },
            ],
            context="Hugo, 16 años, estudiante, 6k€ ingresos.",
        )

    async def test_d3_eligible_user(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Soy elegible para la CaixaBank Travel Gold?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "confirma_elegibilidad",
                    "instruction": (
                        "Confirma que el usuario SÍ cumple los requisitos para "
                        "la Travel Gold (tiene 55k€, necesita 24k€, tiene 38 años)."
                    ),
                },
                {
                    "name": "en_español",
                    "instruction": "Toda la respuesta está en español.",
                },
            ],
            context="Carlos, 55k€ ingresos, 38 años. Travel Gold requiere 24k€ y 18+ años.",
        )

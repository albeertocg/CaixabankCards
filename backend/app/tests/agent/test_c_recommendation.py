"""C – Core recommendation flow tests."""

import pytest

from app.tests.conftest import set_active_user, VIAJERO, SHOPPER_ONLINE, SUPERMERCADO
from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService

RECOMMENDATION_CRITERIA = [
    {
        "name": "nombre_tarjeta",
        "instruction": "Menciona al menos una tarjeta CaixaBank concreta por nombre.",
    },
    {
        "name": "beneficios",
        "instruction": "Explica beneficios relevantes de la tarjeta recomendada.",
    },
    {
        "name": "comisiones",
        "instruction": "Menciona costes o comisiones (cuota anual, porcentajes, etc.).",
    },
    {
        "name": "requisitos",
        "instruction": "Indica requisitos para obtener la tarjeta (ingresos, edad, etc.).",
    },
    {
        "name": "alternativa",
        "instruction": "Ofrece al menos una tarjeta alternativa.",
    },
    {
        "name": "en_español",
        "instruction": "Toda la respuesta está en español.",
    },
]


@pytest.mark.asyncio
class TestRecommendationFlow:
    async def test_c1_viajero_frecuente(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas para mis viajes frecuentes?",
        )

        assert_criteria(
            response=response,
            criteria=[
                *RECOMMENDATION_CRITERIA,
                {
                    "name": "categoria_viajes",
                    "instruction": (
                        "La tarjeta recomendada es de la categoría viajes "
                        "(Travel Classic, Travel Gold o Travel Platinum)."
                    ),
                },
            ],
            context="Carlos, 55k€ ingresos, 38 años, 90% gasto en viajes/transporte.",
        )

    async def test_c2_shopper_online(self, session_shopper, chat: ChatService):
        response = await chat.send_message(
            session_shopper["session_id"],
            "test_user_fixture",
            "Quiero una tarjeta para compras online, ¿cuál me va mejor?",
        )

        assert_criteria(
            response=response,
            criteria=[
                *RECOMMENDATION_CRITERIA,
                {
                    "name": "categoria_compras",
                    "instruction": (
                        "La tarjeta recomendada es de compras online "
                        "(E-Commerce Basic, Advanced o Premium)."
                    ),
                },
            ],
            context="Laura, 32k€ ingresos, 28 años, 80% gasto en compras.",
        )

    async def test_c3_supermercado(self, session_supermercado, chat: ChatService):
        response = await chat.send_message(
            session_supermercado["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me conviene más para el supermercado?",
        )

        assert_criteria(
            response=response,
            criteria=[
                *RECOMMENDATION_CRITERIA,
                {
                    "name": "categoria_super",
                    "instruction": (
                        "La tarjeta recomendada es de supermercado "
                        "(SuperCompra Ahorro, Familia o Gourmet)."
                    ),
                },
            ],
            context="María, 25k€ ingresos, 42 años, 60% gasto en supermercado.",
        )

    async def test_c4_sin_transacciones_ingresos_altos(
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
                *RECOMMENDATION_CRITERIA,
                {
                    "name": "nivel_acorde",
                    "instruction": (
                        "Con 80k€ de ingresos y sin historial, recomienda una tarjeta "
                        "de gama media-alta o premium, no la más básica."
                    ),
                },
            ],
            context="Pedro, 80k€ ingresos, 45 años, SIN transacciones.",
        )

    async def test_c5_sin_transacciones_ingresos_bajos(
        self, session_sin_tx_bajo, chat: ChatService
    ):
        response = await chat.send_message(
            session_sin_tx_bajo["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas?",
        )

        assert_criteria(
            response=response,
            criteria=[
                *RECOMMENDATION_CRITERIA,
                {
                    "name": "nivel_basico",
                    "instruction": (
                        "Con 12k€ de ingresos y estudiante, recomienda una tarjeta "
                        "básica o sin cuota anual, no premium."
                    ),
                },
            ],
            context="Sofía, 12k€ ingresos, 22 años, estudiante, SIN transacciones.",
        )

"""H – Tone and format tests."""

import pytest

from app.tests.helpers.judge import assert_criteria
from app.services.chat_service import ChatService


@pytest.mark.asyncio
class TestToneAndFormat:
    async def test_h1_concise_response(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas para viajes?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "concisa",
                    "instruction": (
                        "La respuesta es concisa y directa. No tiene párrafos "
                        "excesivamente largos ni listas interminables. "
                        "Extensión razonable para una recomendación de chat."
                    ),
                },
            ],
            context="Verificar que la respuesta no es un muro de texto.",
        )

    async def test_h2_formal_conversational_tone(
        self, session_viajero, chat: ChatService
    ):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me conviene más?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "tono_profesional",
                    "instruction": (
                        "El tono es profesional y cercano. Trato de usted o trato "
                        "cercano formal. Sin emojis, sin jerga coloquial excesiva, "
                        "sin lenguaje demasiado técnico."
                    ),
                },
            ],
            context="Verificar tono conversacional pero formal.",
        )

    async def test_h3_no_filler_intros(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "¿Cuál es la mejor tarjeta para viajes?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "sin_relleno",
                    "instruction": (
                        "La respuesta NO empieza con frases de relleno como "
                        "'¡Excelente pregunta!', '¡Claro que sí!', "
                        "'Me alegra que preguntes', 'Con mucho gusto'. "
                        "Va directamente al contenido útil."
                    ),
                },
            ],
            context="Verificar que no hay introducciones innecesarias.",
        )

    async def test_h4_chat_format(self, session_viajero, chat: ChatService):
        response = await chat.send_message(
            session_viajero["session_id"],
            "test_user_fixture",
            "Recomiéndame una tarjeta.",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "formato_chat",
                    "instruction": (
                        "La respuesta tiene formato de conversación de chat: "
                        "frases cortas, separación clara entre secciones. "
                        "No es un documento o ensayo académico."
                    ),
                },
            ],
            context="Verificar formato tipo chat, no documento.",
        )

    async def test_h5_structured_recommendation(
        self, session_shopper, chat: ChatService
    ):
        response = await chat.send_message(
            session_shopper["session_id"],
            "test_user_fixture",
            "¿Qué tarjeta me recomiendas para compras?",
        )

        assert_criteria(
            response=response,
            criteria=[
                {
                    "name": "estructura_clara",
                    "instruction": (
                        "La recomendación presenta la información de forma "
                        "estructurada pero breve: tarjeta recomendada, "
                        "por qué, datos clave, y alternativa. "
                        "Se puede escanear visualmente con facilidad."
                    ),
                },
            ],
            context="Laura, compradora online.",
        )

    async def test_h6_brief_greeting(self, session_viajero):
        greeting = session_viajero["greeting"]

        assert_criteria(
            response=greeting,
            criteria=[
                {
                    "name": "saludo_breve",
                    "instruction": (
                        "El saludo es corto (1-3 frases), profesional, "
                        "y va al tema rápidamente. No es un párrafo largo."
                    ),
                },
            ],
            context="Saludo inicial del agente a Carlos.",
        )

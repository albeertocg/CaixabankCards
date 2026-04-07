"""A – Guardrail tests.

Verify that the input guardrail blocks or allows messages correctly.
"""

import pytest

from app.services.guardrail_service import GuardrailService


@pytest.fixture
def guardrail() -> GuardrailService:
    return GuardrailService()


class TestGuardrailBlocking:
    def test_a1_empty_message(self, guardrail: GuardrailService):
        result = guardrail.validate("")
        assert not result.allowed
        assert (
            "tarjetas" in result.response.lower() or "ayudar" in result.response.lower()
        )

    def test_a1_whitespace_only(self, guardrail: GuardrailService):
        result = guardrail.validate("   ")
        assert not result.allowed

    def test_a2_missing_api_key(self, guardrail: GuardrailService, monkeypatch):
        from app.config.settings import settings

        monkeypatch.setattr(settings, "google_api_key", "")
        result = guardrail.validate("¿Qué tarjeta me recomiendas?")
        assert not result.allowed
        assert (
            "configuración" in result.response.lower()
            or "embeddings" in result.response.lower()
        )

    def test_a3_out_of_scope_weather(self, guardrail: GuardrailService):
        result = guardrail.validate("¿Qué tiempo hace mañana en Barcelona?")
        assert not result.allowed

    def test_a4_out_of_scope_mortgage(self, guardrail: GuardrailService):
        result = guardrail.validate("¿Cuánto me cobran de interés en la hipoteca?")
        assert not result.allowed


class TestGuardrailAllowing:
    def test_a5_card_recommendation_query(self, guardrail: GuardrailService):
        result = guardrail.validate("¿Qué tarjeta me recomiendas para viajes?")
        assert result.allowed

    def test_a5_card_benefits_query(self, guardrail: GuardrailService):
        result = guardrail.validate(
            "¿Cuáles son los beneficios de la tarjeta CaixaBank Oro?"
        )
        assert result.allowed

    def test_a5_card_fees_query(self, guardrail: GuardrailService):
        result = guardrail.validate(
            "¿Cuánto cuesta la cuota anual de las tarjetas de viaje?"
        )
        assert result.allowed

from typing import Any

import pytest

from app.services.gower_service import find_similar_cards
from app.errors.invalid_threshold_error import InvalidThresholdError
from app.errors.invalid_max_results_error import InvalidMaxResultsError


@pytest.fixture
def tarjetas() -> list[dict[str, Any]]:
    return [
        {"nombre": "Visa Oro", "tipo": "crédito", "limite": 5000, "recompensas": "viajes"},
        {"nombre": "Mastercard Clásica", "tipo": "crédito", "limite": 2000, "recompensas": "compras"},
        {"nombre": "Visa Electrón", "tipo": "débito", "limite": 0, "recompensas": "ninguna"},
    ]


@pytest.fixture
def ideal() -> dict[str, Any]:
    return {"nombre": "", "tipo": "crédito", "limite": 4500, "recompensas": "viajes"}


def test_find_similar_cards_basic(tarjetas: list[dict[str, Any]], ideal: dict[str, Any]):
    resultados = find_similar_cards(ideal, tarjetas, threshold=0.5, max_results=2)

    assert isinstance(resultados, list)
    assert 1 <= len(resultados) <= 2
    assert resultados[0]["nombre"] == "Visa Oro"
    assert resultados[0]["tipo"] == "crédito"
    assert resultados[0]["recompensas"] == "viajes"

    # Todos los resultados deben venir de la lista original
    for tarjeta in resultados:
        assert tarjeta in tarjetas


def test_find_similar_cards_threshold(tarjetas: list[dict[str, Any]], ideal: dict[str, Any]):
    resultados = find_similar_cards(ideal, tarjetas, threshold=0.99, max_results=3)
    assert resultados == []


def test_find_similar_cards_invalid_threshold(tarjetas: list[dict[str, Any]], ideal: dict[str, Any]):
    with pytest.raises(InvalidThresholdError):
        find_similar_cards(ideal, tarjetas, threshold=1.5)


def test_find_similar_cards_invalid_max_results(tarjetas: list[dict[str, Any]], ideal: dict[str, Any]):
    with pytest.raises(InvalidMaxResultsError):
        find_similar_cards(ideal, tarjetas, max_results=0)

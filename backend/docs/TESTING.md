# Guía de Testing

## Framework

- **Testing:** `pytest`
- **Cliente HTTP async:** `httpx`
- **Cobertura:** `pytest --cov`

## Estructura real

```
backend/app/tests/
├── conftest.py
├── agent/                        # Suite del agente (evaluación LLM-as-judge)
│   ├── test_a_guardrails.py
│   ├── test_b_context.py
│   ├── test_c_recommendation.py
│   ├── test_d_eligibility.py
│   ├── test_e_category_switch.py
│   ├── test_f_quality.py
│   ├── test_g_edge_cases.py
│   └── test_h_tone_format.py
├── helpers/
│   └── judge.py                  # Judge LLM para evaluar respuestas del agente
└── services/
    └── test_gower_service.py
```

No se utilizan subdirectorios `unit/` e `integration/`: la separación actual es por dominio (`agent/`, `services/`).

## Ejecutar tests

Desde `backend/`:

```bash
pytest app/tests/ -v              # todos los tests
make test                         # equivalente
make test-cov                     # con cobertura (html + terminal)
pytest app/tests/agent/ -v        # solo suite del agente
pytest app/tests/services/ -v     # solo services
pytest -k recommendation          # filtrar por nombre
```

## Convenciones

- Archivos: `test_*.py`
- Funciones: `test_*`
- Fixtures compartidas en `conftest.py`
- Tests del agente usan el helper `judge.py` para puntuar la salida del LLM.

## Cobertura

- **Mínimo esperado:** 80%
- **Objetivo:** 90%
- **Crítico:** 100% en `services/` y `utils/`

El reporte HTML se genera en `htmlcov/` al ejecutar `make test-cov`.

## Requisitos para tests del agente

Los tests de `app/tests/agent/` hacen llamadas reales al LLM (Gemini vía Google ADK), por lo que requieren `GOOGLE_API_KEY` válida en `.env`. Si la API devuelve `503 UNAVAILABLE` (alta demanda), reintentar más tarde.

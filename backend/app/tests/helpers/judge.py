"""LLM-as-judge evaluator using Gemini.

Sends the agent's response + a rubric to Gemini and returns a structured verdict.
"""

import json
import logging

from google import genai

from app.config.settings import settings

logger = logging.getLogger(__name__)

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.google_api_key)
    return _client


JUDGE_SYSTEM = """\
Eres un evaluador imparcial de calidad de respuestas de un chatbot bancario.
Se te proporciona:
- CONTEXTO: información sobre el usuario y la conversación.
- RESPUESTA: la respuesta del chatbot a evaluar.
- CRITERIOS: lista de criterios con nombre e instrucción.

Para CADA criterio devuelve un JSON **estricto** (sin markdown) con esta estructura:
{
  "results": [
    {"criterion": "<nombre>", "pass": true/false, "reason": "<1 frase>"}
  ]
}

Reglas:
- Sé estricto. Solo marca pass=true si el criterio se cumple claramente.
- reason debe ser concisa (máximo 15 palabras).
- Devuelve SOLO el JSON, sin texto adicional, sin bloques de código.\
"""


def judge(
    response: str,
    criteria: list[dict[str, str]],
    context: str = "",
    model: str = "gemini-2.5-flash",
) -> dict[str, dict]:
    """Evaluate a chatbot response against criteria using Gemini as judge.

    Args:
        response: The chatbot response to evaluate.
        criteria: List of dicts with 'name' and 'instruction' keys.
        context: Optional context about the user/conversation.
        model: Gemini model to use for evaluation.

    Returns:
        Dict mapping criterion name to {'pass': bool, 'reason': str}.
    """
    criteria_text = "\n".join(f"- {c['name']}: {c['instruction']}" for c in criteria)

    prompt = (
        f"CONTEXTO:\n{context}\n\nRESPUESTA:\n{response}\n\nCRITERIOS:\n{criteria_text}"
    )

    client = _get_client()
    gemini_response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=JUDGE_SYSTEM,
            temperature=0.0,
        ),
    )

    raw = gemini_response.text.strip()
    # Strip markdown fences if Gemini wraps them anyway
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")]
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Judge returned invalid JSON: %s", raw)
        return {
            c["name"]: {"pass": False, "reason": "Judge returned invalid JSON"}
            for c in criteria
        }

    results: dict[str, dict] = {}
    for item in data.get("results", []):
        results[item["criterion"]] = {
            "pass": item["pass"],
            "reason": item.get("reason", ""),
        }

    for c in criteria:
        if c["name"] not in results:
            results[c["name"]] = {
                "pass": False,
                "reason": "Judge did not evaluate this criterion",
            }

    return results


def assert_criteria(
    response: str,
    criteria: list[dict[str, str]],
    context: str = "",
) -> None:
    """Evaluate and assert all criteria pass.

    Args:
        response: The chatbot response to evaluate.
        criteria: List of dicts with 'name' and 'instruction' keys.
        context: Optional context about the user/conversation.

    Raises:
        AssertionError: If any criterion fails.
    """
    verdicts = judge(response, criteria, context)
    failures = [
        f"  [{name}] {v['reason']}" for name, v in verdicts.items() if not v["pass"]
    ]
    if failures:
        header = f"Criteria failed ({len(failures)}/{len(criteria)}):\n"
        detail = "\n".join(failures)
        raise AssertionError(f"{header}{detail}\n\nResponse was:\n{response[:500]}")

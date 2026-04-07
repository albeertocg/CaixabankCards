from dataclasses import dataclass
from pathlib import Path

from app.agent.rag.embeddings import embed_query
from app.agent.rag.vectorstore import query_semantic
from app.config.settings import settings


@dataclass
class GuardrailResult:
    allowed: bool
    response: str = ""
    best_distance: float | None = None
    matches: list[dict] | None = None


_AGENT_DIR = Path(__file__).resolve().parents[1]
PERSIST_DIR = str(_AGENT_DIR / "agent" / "vectorstore_data")


class GuardrailService:
    def __init__(self, threshold: float = 0.45, max_results: int = 3) -> None:
        self.threshold = threshold
        self.max_results = max_results

    def validate(self, message: str) -> GuardrailResult:
        text = message.strip()

        if not text:
            return GuardrailResult(
                allowed=False,
                response=(
                    "Puedo ayudarte con información sobre tarjetas CaixaBank: "
                    "beneficios, comisiones, requisitos o recomendaciones según tu perfil."
                ),
            )

        if not settings.google_api_key.strip():
            return GuardrailResult(
                allowed=False,
                response=(
                    "Ahora mismo no puedo validar la consulta porque falta la configuración "
                    "del servicio de embeddings."
                ),
            )

        query_vector = embed_query(text, api_key=settings.google_api_key)
        results = query_semantic(
            query_embedding=query_vector,
            persist_dir=PERSIST_DIR,
            max_results=self.max_results,
        )

        if not results:
            return GuardrailResult(
                allowed=False,
                response=self.out_of_scope_response(),
                matches=[],
            )

        best_distance = results[0]["distance"]

        print(
            f"[GUARDRAIL] message={text!r} "
            f"best_distance={best_distance:.4f} "
            f"threshold={self.threshold}"
        )
        print(f"[GUARDRAIL] validando: {text!r}")
        print(f"[GUARDRAIL] best_distance={best_distance}")
        if best_distance > self.threshold:
            return GuardrailResult(
                allowed=False,
                response=self.out_of_scope_response(),
                best_distance=best_distance,
                matches=results,
            )

        return GuardrailResult(
            allowed=True,
            best_distance=best_distance,
            matches=results,
        )

    @staticmethod
    def out_of_scope_response() -> str:
        return (
            "Solo puedo ayudarte con consultas relacionadas con tarjetas CaixaBank. "
            "Puedo explicarte beneficios, comisiones, requisitos o recomendarte una tarjeta."
        )
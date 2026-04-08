from dataclasses import dataclass
import logging
from pathlib import Path

from app.agent.rag.embeddings import embed_query
from app.agent.rag.vectorstore import query_semantic
from app.config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class GuardrailResult:
    allowed: bool
    response: str = ""
    best_distance: float | None = None
    matches: list[dict] | None = None


_AGENT_DIR = Path(__file__).resolve().parents[1]
PERSIST_DIR = str(_AGENT_DIR / "agent" / "vectorstore_data")


class GuardrailService:
    # Threshold for first messages in a conversation (stricter)
    DEFAULT_THRESHOLD = 0.35
    # Relaxed threshold for follow-up messages in an existing session
    FOLLOWUP_THRESHOLD = 0.42

    def __init__(
        self,
        threshold: float = DEFAULT_THRESHOLD,
        max_results: int = 3,
    ) -> None:
        self.threshold = threshold
        self.max_results = max_results

    def validate(self, message: str, *, is_followup: bool = False) -> GuardrailResult:
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
        effective_threshold = self.FOLLOWUP_THRESHOLD if is_followup else self.threshold

        logger.debug(
            "message=%s best_distance=%.4f threshold=%.2f followup=%s",
            text,
            best_distance,
            effective_threshold,
            is_followup,
        )
        if best_distance > effective_threshold:
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

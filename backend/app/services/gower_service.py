from typing import Any

import pandas as pd
import gower_exp as gower

from app.errors.invalid_threshold_error import InvalidThresholdError
from app.errors.invalid_max_results_error import InvalidMaxResultsError


# =========================
# Public API
# =========================
def find_similar_cards(
    ideal_card: dict[str, Any],
    available_cards: list[dict[str, Any]],
    threshold: float = 0.5,
    max_results: int = 5,
) -> list[dict[str, Any]]:
    """Find credit cards similar to an ideal card using Gower distance.

    Note:
        `gower_exp.gower_topn` returns distances in `values`:
        - 0.0 means identical (best)
        - 1.0 means very different (worst)

        This function converts distances to similarity with:
        `similarity = 1 - distance`.

    Args:
        ideal_card: Ideal card features as a mapping.
        available_cards: Candidate cards, each as a mapping of features.
        threshold: Similarity threshold in [0, 1]. Higher means stricter.
        max_results: Maximum number of results to return.

    Returns:
        A list of cards (dicts) sorted by similarity (descending), filtered by threshold.

    Raises:
        InvalidThresholdError: If threshold is not within [0, 1].
        InvalidMaxResultsError: If max_results is not a positive integer.
    """
    if not (0.0 <= threshold <= 1.0):
        raise InvalidThresholdError(f"Threshold must be between 0 and 1. Got {threshold}.")
    if max_results <= 0:
        raise InvalidMaxResultsError(f"max_results must be a positive integer. Got {max_results}.")

    ideal_card_dataframe, available_cards_dataframe = _build_aligned_dataframes(
        ideal_card=ideal_card,
        available_cards=available_cards,
    )

    top_n = min(max_results, len(available_cards_dataframe))
    indices_and_similarities = _topn_indices_and_similarities(
        ideal_card_dataframe=ideal_card_dataframe,
        available_cards_dataframe=available_cards_dataframe,
        top_n=top_n,
    )

    filtered = [
        (card_index, similarity) for card_index, similarity in indices_and_similarities if similarity >= threshold
    ]
    filtered.sort(key=lambda pair: pair[1], reverse=True)

    return [dict(available_cards[card_index]) for card_index, _ in filtered]


# =========================
# Private helpers
# =========================
def _build_aligned_dataframes(
    ideal_card: dict[str, Any],
    available_cards: list[dict[str, Any]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    available_cards_dataframe = pd.DataFrame(list(available_cards))
    ideal_card_dataframe = pd.DataFrame([ideal_card])

    all_columns = sorted(set(available_cards_dataframe.columns).union(ideal_card_dataframe.columns))
    available_cards_dataframe = available_cards_dataframe.reindex(columns=all_columns)
    ideal_card_dataframe = ideal_card_dataframe.reindex(columns=all_columns)

    numeric_columns = available_cards_dataframe.select_dtypes(include="number").columns
    categorical_columns = [col for col in all_columns if col not in set(numeric_columns)]

    available_cards_dataframe[numeric_columns] = available_cards_dataframe[numeric_columns].fillna(0.0)
    ideal_card_dataframe[numeric_columns] = ideal_card_dataframe[numeric_columns].fillna(0.0)

    available_cards_dataframe[categorical_columns] = available_cards_dataframe[categorical_columns].fillna("MISSING")
    ideal_card_dataframe[categorical_columns] = ideal_card_dataframe[categorical_columns].fillna("MISSING")

    return ideal_card_dataframe, available_cards_dataframe


def _topn_indices_and_similarities(
    ideal_card_dataframe: pd.DataFrame,
    available_cards_dataframe: pd.DataFrame,
    top_n: int,
) -> list[tuple[int, float]]:
    topn_result = gower.gower_topn(ideal_card_dataframe, available_cards_dataframe, n=top_n)

    nearest_indices = list(topn_result["index"])
    nearest_distances = list(topn_result["values"])

    nearest_similarities = [1.0 - float(distance) for distance in nearest_distances]
    return [
        (int(card_index), float(similarity)) for card_index, similarity in zip(nearest_indices, nearest_similarities)
    ]

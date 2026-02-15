"""Grade extraction from LLM responses."""

import re
from dataclasses import dataclass

from .rubric import Criterion


@dataclass
class Grade:
    """A single extracted grade for one criterion."""

    criterion: str
    score: int | None
    max_points: int


def extract_grades(response: str, criteria: list[Criterion]) -> list[Grade]:
    """Extract numerical grades from an LLM response based on rubric criteria.

    For each criterion, searches the response for patterns like
    ``Criterion Name: 8/10`` or ``Criterion Name ... 8/10``.
    Searches from the end of the response first, since LLMs typically
    place summary scores at the end.
    """
    grades = []

    for criterion in criteria:
        score = _find_score(response, criterion.name, criterion.points)
        grades.append(
            Grade(
                criterion=criterion.name,
                score=score,
                max_points=criterion.points,
            )
        )

    return grades


def _find_score(text: str, criterion_name: str, max_points: int) -> int | None:
    """Find a score for a criterion in the response text.

    Strategy:
    1. Find all occurrences of the criterion name (case-insensitive).
    2. Starting from the last occurrence, look for ``X/<max_points>``
       within 300 characters.
    3. Return the first valid score found, or None.
    """
    escaped_name = re.escape(criterion_name)
    matches = list(re.finditer(escaped_name, text, re.IGNORECASE))

    if not matches:
        return None

    for name_match in reversed(matches):
        region = text[name_match.start() : name_match.start() + 300]
        score_match = re.search(rf"(\d+)\s*/\s*{max_points}", region)
        if score_match:
            score = int(score_match.group(1))
            if 0 <= score <= max_points:
                return score

    return None

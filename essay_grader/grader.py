"""Core grading orchestration."""

import logging
import time
from dataclasses import dataclass
from pathlib import Path

from .llm import LLMProvider
from .parsing import Grade, extract_grades
from .readers import read_file
from .rubric import Rubric

logger = logging.getLogger(__name__)


@dataclass
class GradingResult:
    """Result of grading a single submission."""

    file: str
    response: str
    grades: list[Grade]

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "grades": {
                g.criterion: {"score": g.score, "max_points": g.max_points}
                for g in self.grades
            },
            "response": self.response,
        }


def grade_submission(
    rubric: Rubric,
    provider: LLMProvider,
    submission_path: str | Path,
    template_vars: dict[str, str] | None = None,
) -> GradingResult:
    """Grade a single submission.

    Args:
        rubric: The loaded rubric with criteria and prompt template.
        provider: The LLM provider to use.
        submission_path: Path to the essay file (PDF or text).
        template_vars: Extra template variables beyond ``essay``.
    """
    submission_path = Path(submission_path)
    essay_text = read_file(submission_path)

    variables = {"essay": essay_text}
    if template_vars:
        variables.update(template_vars)

    prompt = rubric.render(**variables)
    logger.info("Grading %s...", submission_path.name)

    response = provider.complete(prompt)
    grades = extract_grades(response, rubric.criteria)

    return GradingResult(
        file=str(submission_path),
        response=response,
        grades=grades,
    )


def grade_batch(
    rubric: Rubric,
    provider: LLMProvider,
    input_dir: str | Path,
    template_vars: dict[str, str] | None = None,
    delay: float = 1.0,
) -> list[GradingResult]:
    """Grade all submissions in a directory.

    Args:
        rubric: The loaded rubric.
        provider: The LLM provider to use.
        input_dir: Directory containing essay files.
        template_vars: Extra template variables beyond ``essay``.
        delay: Seconds to wait between API calls (rate limiting).
    """
    input_dir = Path(input_dir)
    files = sorted(f for f in input_dir.iterdir() if f.is_file())

    if not files:
        logger.warning("No files found in %s", input_dir)
        return []

    results = []
    for i, file_path in enumerate(files):
        result = grade_submission(rubric, provider, file_path, template_vars)
        results.append(result)

        if delay > 0 and i < len(files) - 1:
            time.sleep(delay)

    return results

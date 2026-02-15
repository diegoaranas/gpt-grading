"""Rubric template loading and rendering."""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jinja2 import Template


@dataclass
class Criterion:
    """A single grading criterion."""

    name: str
    points: int
    description: str = ""


@dataclass
class Rubric:
    """A grading rubric with criteria and a prompt template.

    Rubrics are loaded from markdown files with YAML frontmatter:

        ---
        criteria:
          - name: "Clarity"
            points: 10
            description: "Is the writing clear?"
          - name: "Grammar"
            points: 5
        ---
        Grade the following essay...
        {{ essay }}
    """

    criteria: list[Criterion]
    template: str

    def render(self, **variables: str) -> str:
        """Render the prompt template with the given variables.

        The most common variable is ``essay`` (the student's text), but
        rubric templates can reference any variable name.
        """
        return Template(self.template).render(**variables)


def load_rubric(path: str | Path) -> Rubric:
    """Load a rubric from a markdown file with YAML frontmatter.

    The file must begin with a ``---`` delimited YAML block containing
    at least a ``criteria`` list, followed by the prompt template body.
    """
    path = Path(path)
    text = path.read_text()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        raise ValueError(
            f"Rubric file {path} must have YAML frontmatter delimited by ---"
        )

    frontmatter = yaml.safe_load(match.group(1))
    template_body = match.group(2)

    raw_criteria = frontmatter.get("criteria")
    if not raw_criteria:
        raise ValueError(f"Rubric file {path} must define at least one criterion")

    criteria = [
        Criterion(
            name=c["name"],
            points=c["points"],
            description=c.get("description", ""),
        )
        for c in raw_criteria
    ]

    return Rubric(criteria=criteria, template=template_body)

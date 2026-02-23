"""CLI interface for essay-grader."""

import csv
import json
import logging
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

from .grader import grade_batch, grade_submission
from .llm import create_provider
from .rubric import load_rubric


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging.")
def main(verbose: bool) -> None:
    """Essay Grader - Grade essays using LLMs with customizable rubric templates."""
    load_dotenv()
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
    )


@main.command()
@click.option(
    "--rubric",
    "-r",
    required=True,
    type=click.Path(exists=True),
    help="Path to rubric template (markdown with YAML frontmatter).",
)
@click.option(
    "--input",
    "-i",
    "input_path",
    required=True,
    type=click.Path(exists=True),
    help="Input file or directory of essays.",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(),
    default=None,
    help="Output file (single) or directory (batch). Prints to stdout if omitted.",
)
@click.option(
    "--provider",
    "-p",
    default="openai",
    type=click.Choice(["openai", "anthropic"]),
    help="LLM provider.",
)
@click.option("--model", "-m", default=None, help="Model name (provider-specific).")
@click.option("--api-key", default=None, help="API key (overrides env variable).")
@click.option(
    "--delay",
    "-d",
    default=1.0,
    type=float,
    help="Seconds between API calls in batch mode.",
)
@click.option(
    "--var",
    multiple=True,
    help="Template variable as key=value (repeatable).",
)
@click.option(
    "--var-file",
    multiple=True,
    help="Template variable loaded from a file as key=path (repeatable).",
)
@click.option(
    "--output-format",
    "fmt",
    default="text",
    type=click.Choice(["text", "json", "csv"]),
    help="Output format.",
)
def grade(
    rubric: str,
    input_path: str,
    output_path: str | None,
    provider: str,
    model: str | None,
    api_key: str | None,
    delay: float,
    var: tuple[str, ...],
    var_file: tuple[str, ...],
    fmt: str,
) -> None:
    """Grade essay(s) using a rubric template."""
    rubric_obj = load_rubric(rubric)
    llm = create_provider(provider, model=model, api_key=api_key)

    template_vars = _parse_template_vars(var, var_file)
    input_p = Path(input_path)

    if input_p.is_file():
        _grade_single(rubric_obj, llm, input_p, template_vars, fmt, output_path)
    elif input_p.is_dir():
        _grade_batch(rubric_obj, llm, input_p, template_vars, fmt, output_path, delay)
    else:
        raise click.BadParameter(f"{input_path} is neither a file nor directory")


def _parse_template_vars(
    var: tuple[str, ...], var_file: tuple[str, ...]
) -> dict[str, str]:
    """Parse --var and --var-file options into a dict."""
    template_vars: dict[str, str] = {}

    for v in var:
        key, sep, value = v.partition("=")
        if not sep:
            raise click.BadParameter(f"--var must be key=value, got: {v}")
        template_vars[key] = value

    for vf in var_file:
        key, sep, path = vf.partition("=")
        if not sep:
            raise click.BadParameter(f"--var-file must be key=path, got: {vf}")
        template_vars[key] = Path(path).read_text()

    return template_vars


def _grade_single(rubric_obj, llm, input_p, template_vars, fmt, output_path):
    """Grade a single file and output the result."""
    result = grade_submission(rubric_obj, llm, input_p, template_vars)

    if fmt == "json":
        output = json.dumps(result.to_dict(), indent=2)
    elif fmt == "csv":
        lines = ["criterion,score,max_points"]
        for g in result.grades:
            lines.append(f"{g.criterion},{g.score},{g.max_points}")
        output = "\n".join(lines)
    else:
        output = result.response

    if output_path:
        Path(output_path).write_text(output)
        click.echo(f"Grade saved to {output_path}")
    else:
        click.echo(output)


def _grade_batch(rubric_obj, llm, input_p, template_vars, fmt, output_path, delay):
    """Grade all files in a directory and output results."""
    results = grade_batch(
        rubric_obj, llm, input_p, template_vars=template_vars, delay=delay
    )

    if not results:
        click.echo("No files found to grade.")
        return

    if fmt == "csv":
        _write_csv(results, output_path)
    elif output_path:
        out_dir = Path(output_path)
        out_dir.mkdir(parents=True, exist_ok=True)

        ext = ".json" if fmt == "json" else ".txt"
        for r in results:
            stem = Path(r.file).stem
            out_file = out_dir / f"{stem}{ext}"
            if fmt == "json":
                out_file.write_text(json.dumps(r.to_dict(), indent=2))
            else:
                out_file.write_text(r.response)

        click.echo(f"Grades saved to {out_dir}")
    else:
        for r in results:
            click.echo(f"\n{'=' * 60}")
            click.echo(f"File: {r.file}")
            click.echo(f"{'=' * 60}")
            click.echo(r.response)


def _write_csv(results, output_path):
    """Write batch results to CSV."""
    criteria_names = [g.criterion for g in results[0].grades]

    if output_path:
        f = open(output_path, "w", newline="")
    else:
        f = sys.stdout

    try:
        writer = csv.writer(f)
        writer.writerow(["file"] + criteria_names)
        for r in results:
            row = [Path(r.file).name]
            for g in r.grades:
                row.append(g.score if g.score is not None else "")
            writer.writerow(row)
    finally:
        if output_path:
            f.close()
            click.echo(f"Grades saved to {output_path}")

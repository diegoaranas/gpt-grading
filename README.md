# essay-grader

Grade essays using LLMs with customizable rubric templates.

Define your grading rubric as a Markdown file, point it at a folder of essays, and get structured grades back. Supports multiple LLM providers (OpenAI, Anthropic) and input formats (PDF, plain text).

## Installation

Requires Python 3.10+.

```bash
pip install -e .                    # core (no LLM providers)
pip install -e ".[openai]"          # with OpenAI support
pip install -e ".[anthropic]"       # with Anthropic support
pip install -e ".[all]"             # with all providers
```

Set your API key as an environment variable or in a `.env` file:

```bash
# For OpenAI
OPENAI_API_KEY=sk-...

# For Anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

## Quick Start

### 1. Create a rubric template

Rubrics are Markdown files with YAML frontmatter. The frontmatter defines grading criteria (name + max points). The body is the prompt sent to the LLM, with Jinja2 template variables.

```markdown
---
criteria:
  - name: "Thesis"
    points: 20
  - name: "Evidence"
    points: 30
  - name: "Writing Quality"
    points: 20
  - name: "Overall"
    points: 100
---
Grade the following essay. For each criterion, provide a brief
assessment and a score in the format "X/Y".

## Rubric
- **Thesis**: /20 (is the thesis clear and arguable?)
- **Evidence**: /30 (is the evidence relevant and sufficient?)
- **Writing Quality**: /20 (clarity, grammar, structure)
- **Overall**: /100

## Essay

{{ essay }}

Grade the essay above.
```

See `examples/philosophy_rubric.md` for a more detailed example.

### 2. Grade essays

```bash
# Grade a single essay
essay-grader grade --rubric rubric.md --input essay.pdf

# Grade a folder of essays, save results
essay-grader grade --rubric rubric.md --input ./submissions/ --output ./grades/

# Use Anthropic instead of OpenAI
essay-grader grade --rubric rubric.md --input essay.txt --provider anthropic

# Specify a model
essay-grader grade --rubric rubric.md --input essay.pdf --model gpt-4o-mini

# Output as JSON
essay-grader grade --rubric rubric.md --input essay.pdf --output-format json

# Batch grade to CSV
essay-grader grade --rubric rubric.md --input ./submissions/ --output grades.csv --output-format csv
```

### 3. Pass extra template variables

Rubric templates can use any Jinja2 variable. Pass them via `--var` (inline) or `--var-file` (from a file):

```bash
essay-grader grade \
  --rubric rubric.md \
  --input essay.pdf \
  --var-file instructions=assignment_instructions.txt \
  --var-file reference_text=source_passage.txt
```

## CLI Reference

```
essay-grader grade [OPTIONS]

Options:
  -r, --rubric PATH        Rubric template file (required)
  -i, --input PATH         Input file or directory (required)
  -o, --output PATH        Output file/directory (stdout if omitted)
  -p, --provider TEXT      LLM provider: openai, anthropic (default: openai)
  -m, --model TEXT         Model name (provider default if omitted)
  --api-key TEXT           API key (overrides env variable)
  -d, --delay FLOAT        Seconds between API calls in batch mode (default: 1.0)
  --var TEXT               Template variable as key=value (repeatable)
  --var-file TEXT          Template variable from file as key=path (repeatable)
  --output-format TEXT     Output format: text, json, csv (default: text)
  -v, --verbose            Enable verbose logging
```

## Rubric Template Format

A rubric template is a Markdown file with two parts:

**YAML frontmatter** defines the criteria the parser will extract from LLM responses:

```yaml
---
criteria:
  - name: "Criterion Name"    # used to find scores in LLM output
    points: 10                 # max points (used to match "X/10" patterns)
    description: "Optional"    # for documentation, not sent to LLM
---
```

**Markdown body** is the prompt template. Use Jinja2 syntax for variables:

- `{{ essay }}` — automatically filled with the submission text
- `{{ any_variable }}` — filled via `--var` or `--var-file` CLI options
- `{% if variable %}...{% endif %}` — conditional sections

The parser extracts grades by searching the LLM response for each criterion name followed by a score pattern like `8/10`.

## Project Structure

```
essay_grader/
├── __init__.py       # Package version
├── __main__.py       # python -m essay_grader
├── cli.py            # Click CLI
├── grader.py         # Core orchestration
├── rubric.py         # Rubric loading & rendering
├── readers.py        # PDF + text file readers
├── parsing.py        # Grade extraction from LLM responses
└── llm/
    ├── __init__.py   # Provider registry
    ├── base.py       # Abstract provider interface
    ├── openai.py     # OpenAI provider
    └── anthropic.py  # Anthropic provider
```

## License

MIT

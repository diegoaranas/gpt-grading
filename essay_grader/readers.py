"""File readers for different input formats."""

from pathlib import Path

PDF_EXTENSIONS = {".pdf"}
TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".text", ".rst"}


def read_file(path: str | Path) -> str:
    """Read a file and return its text content.

    Dispatches to the appropriate reader based on file extension.
    Supports PDF and plain-text formats.
    """
    path = Path(path)

    if path.suffix.lower() in PDF_EXTENSIONS:
        return _read_pdf(path)
    else:
        return _read_text(path)


def _read_pdf(path: Path) -> str:
    """Read a PDF file and return its text content."""
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError(
            "pypdf package is required to read PDF files. "
            "Install it with: pip install pypdf"
        )

    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def _read_text(path: Path) -> str:
    """Read a plain text file."""
    return path.read_text()

from pypdf import PdfReader

def read_pdf(file_path: str) -> str:
    """
    Reads PDF files

    Args:
        file_path (str): Path to PDF file

    Returns:
        str: Text from PDF file
    """
    # Load PDF file
    reader = PdfReader(file_path)

    # Read PDF file
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Output text
    return text
from pypdf import PdfReader
import io
from requests import Response


def clean_string(string: str) -> str:
    """Removes special characters like line feed and zero width space
    from a string.
    Args:
        string (str): string

    Returns:
        str: Clean string
    """
    NON_BREAK_SPACE_CHAR = u'\xa0'
    LF_CHAR = u'\n'  # line feed
    EOL_CHAR = u'\r\n'  # end of line
    ZERO_WIDTH_SPACE = u'\u200b'

    string = (string.strip()
              .replace(EOL_CHAR, ' ')
              .replace(NON_BREAK_SPACE_CHAR, ' ')
              .replace(ZERO_WIDTH_SPACE, '')
              .replace(LF_CHAR, '')
              )
    return string.strip()


def extract_text(pdf_response: Response) -> str:
    """Extract text from a PDF file

    Args:
        response (object): HTML response after requesting PDF through its URL

    Returns:
        string: A string with all text content in pdf
    """
    if pdf_response.status_code != 200:
        return ""

    pdf_text = ""

    with io.BytesIO(pdf_response.content) as open_pdf_file:
        reader = PdfReader(open_pdf_file)
        page_count = len(reader.pages)

        for pageNum in range(0, page_count):
            page = reader.pages[pageNum]
            pdf_text += page.extract_text()
    return pdf_text

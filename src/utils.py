from pypdf import PdfReader
import io
from scraper.request_helper import request
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


def has_keyword(pdf_text: str) -> bool:
    """Returns True if text contains at least 1 keyword from `filters.txt` or
    `filters.txt` file is empty.

    Args:
        pdf_text (str): A string of text content in a PDF

    Returns:
        bool
    """
    # Replace U+2019 char with '
    pdf_text = pdf_text.replace('’', "'")

    line_count = 0
    with open('data/filters.txt', 'r') as f:
        for keyword in f:
            line_count += 1
            if keyword.strip().lower() in pdf_text.lower().split(' '):
                return True
    if line_count == 0:
        return True
    return False


if __name__ == "__main__":
    test = ['\u200bSTATE', 'OF', 'MAURITIUS',
            'POSTGRADUATE', 'SCHOLARSHIP', 'SCHEME', '2022/2023']
    print(clean_string(' '.join(test)))

    URL = ('https://education.govmu.org/Documents/2022/scholarship/'
           'Communique-UK%20Commonwealth.doc.pdf')
    txt = extract_text(request(URL))
    print(has_keyword(txt))

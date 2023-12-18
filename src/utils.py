import PyPDF2
import io
from requestfunction import make_request


def clean_string(string: str) -> str:
    """Removes special characters like line feed, zero width space, ...
        from a string.
    Args:
        name (str): original scholarship name directly from html

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


def extract_text(response):
    """Extract text from a PDF file

    Args:
        response (object): HTML response after requesting PDF through its URL

    Returns:
        string: A string with all text content in pdf
    """
    PDF_text = ""

    with io.BytesIO(response.content) as open_pdf_file:
        reader = PyPDF2.PdfFileReader(open_pdf_file)
        page_count = reader.getNumPages()

        for pageNum in range(0, page_count):
            page = reader.pages[pageNum]
            PDF_text += page.extract_text()
    return PDF_text


def is_keyword_compliant(PDF_text: str) -> bool:
    """Returns True if text contains at least 1 keyword from `keywords.txt` or
    `keywords.txt` file is empty.

    Args:
        PDF_text (str): A string of text content in a PDF

    Returns:
        bool
    """
    # Replace U+2019 char with '
    PDF_text = PDF_text.replace('’', "'")

    line_count = 0
    with open('data/keywords.txt', 'r') as f:
        for keyword in f:
            line_count += 1
            if keyword.strip().lower() in PDF_text.lower().split(' '):
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
    txt = extract_text(make_request(URL))
    print(is_keyword_compliant(txt))

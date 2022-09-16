#!venv/bin/python3
import PyPDF2
import io
from requestfunction import makeRequest

def getPDFtext(response):
    """_summary_

    Args:
        response (object): HTML response after requesting a URL

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

def validPDF(PDF_text):
    """Returns True if pdf contains at least 1 keyword from keywords.txt. 
    If text file is empty, always return true.

    Args:
        PDF_text (string): A string of all text content in pdf

    Returns:
        boolean
    """
    # Replace U+2019 char with '
    PDF_text = PDF_text.replace('’',"'")

    line_count = 0
    with open('data/keywords.txt', 'r') as f:
        for keyword in f:
            line_count+=1
            if keyword.strip().lower() in PDF_text.lower().split(' '):
                return True
    # print("number of lines =",line_count)
    if line_count == 0 :
        return True
    return False


if __name__ == "__main__":
    URL = 'https://education.govmu.org/Documents/2022/scholarship/Communique-UK%20Commonwealth.doc.pdf'
    txt = getPDFtext(makeRequest(URL))
    print(validPDF(txt))

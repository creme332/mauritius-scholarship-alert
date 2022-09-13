#!venv/bin/python3
import PyPDF2
import io
from requestfunc import makeRequest


def getPDFtext(response):
    PDF_text = ""

    with io.BytesIO(response.content) as open_pdf_file:
        reader = PyPDF2.PdfFileReader(open_pdf_file)
        page_count = reader.getNumPages()

        for pageNum in range(0, page_count):
            page = reader.pages[pageNum]
            PDF_text += page.extract_text()
    return PDF_text


def getKeywordsFromPDF(PDF_text):
    TEST_KEYWORDS = ['undergraduate',
                     'postgraduate', 'bachelor', "master’s",
                     'phd']
    matched_keywords = []
    response = ""
    # print(all_words)
    # find matching keywords
    for keyword in TEST_KEYWORDS:
        if keyword.lower() in PDF_text.lower():
            matched_keywords.append(keyword)
    return matched_keywords


if __name__ == "__main__":
    URL = 'https://education.govmu.org/Documents/2022/scholarship/Communique-UK%20Commonwealth.doc.pdf'
    print(getPDFtext(makeRequest(URL)).split('\n \n')[1])

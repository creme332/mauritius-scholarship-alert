#!venv/bin/python3
import requests
import PyPDF2
import io

def getKeywordsFromPDF(URL):
    TEST_KEYWORDS = ['undergraduate',
    'postgraduate','bachelor',"master’s",
    'phd']
    matched_keywords = []
    PDF_text = ""
    response = requests.get(URL)

    with io.BytesIO(response.content) as open_pdf_file:
        reader = PyPDF2.PdfFileReader(open_pdf_file)
        page_count = reader.getNumPages()

        for pageNum in range(0,page_count):
            page = reader.pages[pageNum]
            PDF_text += page.extract_text()
            # print(all_words)
            # find matching keywords
            # for keyword in TEST_KEYWORDS:
            #     if keyword.lower() in all_words:
            #         matched_keywords.append(keyword)
    return PDF_text



URL = 'https://education.govmu.org/Documents/2022/scholarship/Communique-UK%20Commonwealth.doc.pdf'
print(getKeywordsFromPDF(URL))

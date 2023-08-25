from pdf_reader import reader


def test_pdf_to_text_tesseract():
    pdf_bytes = open('tests/sample.pdf', 'rb').read()
    assert reader.pdf_to_text_tesseract(pdf_bytes) == "Halohalo test 123\n455"
    
    
def test_docx_to_text():
    docx_bytes = open('tests/sample.docx', 'rb').read()
    assert reader.docx_to_text(docx_bytes) == "Halohalo test 123\n455"
    
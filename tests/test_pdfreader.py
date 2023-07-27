from pdf_reader import reader

pdf_text = """
Haloudasobdfas
Asnfiapsnf

lasf

Nasfias

ni
"""


def test_pdfreader():
    pdf_contents: bytes = open('tests/sample.pdf', 'rb').read()
    assert reader.pdf_to_text_tesseract(pdf_contents) == pdf_text.strip()
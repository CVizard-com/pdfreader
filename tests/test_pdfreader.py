from pdf_reader import reader

pdf_text = """
A Simple PDF File

This is a small demonstration .pdf file -

just for use in the Virtual Mechanics tutorials. More text. And more
text. And more text. And more text. And more text.

And more text. And more text. And more text. And more text. And more
text. And more text. Boring, zzzzz. And more text. And more text. And
more text. And more text. And more text. And more text. And more text.
And more text. And more text.

And more text. And more text. And more text. And more text. And more
text. And more text. And more text. Even more. Continued on page 2...
Simple PDF File 2

..continued from page 1. Yet more text. And more text. And more text.
And more text. And more text. And more text. And more text. And more
text. Oh, how boring typing this stuff. But not as boring as watching
paint dry. And more text. And more text. And more text. And more text.
Boring. More, a little more text. The end, and just as well.
"""


def test_pdfreader():
    pdf_contents: bytes = open('tests/test_pdf_file.pdf', 'rb').read()
    pdf_correct_text: str = open('tests/test_pdf_file.txt', 'r').read()
    assert reader.pdf_to_text_tesseract(pdf_contents) == pdf_correct_text.strip()
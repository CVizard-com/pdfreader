from pdf_reader import reader

pdf_text = """
Adobe Acrobat PDF Files

Adobe® Portable Document Format (PDF) is a universal file format that preserves all
of the fonts, formatting, colours and graphics of any source document, regardless of
the application and platform used to create it.

Adobe PDF is an ideal format for electronic document distribution as it overcomes the
problems commonly encountered with electronic file sharing.

¢ Anyone, anywhere can open a PDF file. All you need is the free Adobe Acrobat
Reader. Recipients of other file formats sometimes can't open files because they
don't have the applications used to create the documents.

¢ PDF files always print correctly on any printing device.
¢ PDF files always display exactly as created, regardless of fonts, software, and
operating systems. Fonts, and graphics are not lost due to platform, software, and

version incompatibilities.

* The free Acrobat Reader is easy to download and can be freely distributed by
anyone.

* Compact PDF files are smaller than their source files and download a
page at a time for fast display on the Web.
"""


def test_pdfreader():
    pdf_contents: bytes = open('tests/pdf-sample.pdf', 'rb').read()
    assert reader.pdf_to_text_tesseract(pdf_contents) == pdf_text.strip()
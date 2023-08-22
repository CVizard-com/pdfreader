import pytesseract
from pdf2image.pdf2image import convert_from_bytes
from PIL import Image
from tempfile import TemporaryDirectory
from pypdf import PdfReader
from io import BytesIO


TESSERACT_OPTIONS = '-l eng+pol'


def pdf_to_text_tesseract(pdf_bytes: bytes, tesseract_options=TESSERACT_OPTIONS) -> str:
    with TemporaryDirectory() as tempdir:
        pdf_pages = convert_from_bytes(pdf_bytes, fmt='png', output_folder=tempdir, dpi=300)
        image_file_list = []
        text = ''

        for page_enumeration, page in enumerate(pdf_pages):
            image_path = f'{tempdir}/{page_enumeration}.png'
            page.save(image_path, 'PNG')
            image_file_list.append(image_path)


        for image_file in image_file_list:
            page_text = pytesseract.image_to_string(Image.open(image_file), config=tesseract_options)
            text += page_text

        return text.strip()
    

def pdf_to_text_pypdf(pdf_bytes: bytes) -> str:
    with BytesIO(pdf_bytes) as pdf_file:
        pdf = PdfReader(pdf_file)
        text = ''

        for page in pdf.pages:
            text += page.extract_text()

        return text
    

if __name__ == '__main__':
    pdf_file = open('test.pdf', 'rb')
    pdf_bytes = pdf_file.read()
    text = pdf_to_text_pypdf(pdf_bytes)
    print(text)
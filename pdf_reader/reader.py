import io
import pytesseract
from pdf2image.pdf2image import convert_from_bytes
from PIL import Image
from tempfile import TemporaryDirectory
import textract
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
    
def docx_to_text(docx_bytes) -> str:
    with TemporaryDirectory() as tempdir:
        docx_path = f'{tempdir}/file.docx'
        with open(docx_path, 'wb') as docx_file:
            docx_file.write(docx_bytes)

        fullText = textract.process(docx_path)
        return fullText.decode('utf-8').strip()
        


if __name__ == '__main__':
    #pdf_file = open('cv-kempinski.pdf', 'rb')
    with open ('jd.docx', 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()
        print(docx_to_text(pdf_bytes))
   
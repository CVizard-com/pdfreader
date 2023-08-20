import uuid
import logging
from fastapi import (
    FastAPI,
    UploadFile, 
    Request, 
    status,
    Request,
    Body,
    Form,
    Depends
    )
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from pdf_reader.reader import pdf_to_text_tesseract, docx_to_text
from pdf_reader.exceptions import KafkaUploadException
import os
from fastapi.middleware.cors import CORSMiddleware
from pdf_reader.kafka_producer import create_kafka_producer

app = FastAPI()


bootstrap_servers = os.environ['BOOTSTRAP_SERVERS']
topic_name = os.environ['PDF_TEXT_TOPIC']


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_kafka_producer():
    return create_kafka_producer(bootstrap_servers)


@app.exception_handler(KafkaUploadException)
async def kafka_exception_handler(request: Request, exc: KafkaUploadException):
    return JSONResponse(
        status_code=500,
        content={"message": f"Something went wrong: {exc.name}"},
    )


@app.post('/api/reader')
async def upload_pdf_file(file: UploadFile = Form(...), id: str = Form(...), kafka = Depends(get_kafka_producer)):
    file_extension = file.filename.split('.')[-1]
    text = ''

    if file_extension != 'pdf':
        contents = await file.read()
        text = docx_to_text(contents)
    else:
        pdf_contents = await file.read()
        text = pdf_to_text_tesseract(pdf_contents)
    try:
        future = kafka.send(topic_name, key=id.encode('utf-8'), value=text.encode('utf-8'))
        return {"file_id": id}
    except Exception as e:
        logging.error(f"could not add event to kafka error has been thrown {e}")
        raise KafkaUploadException(name=e)
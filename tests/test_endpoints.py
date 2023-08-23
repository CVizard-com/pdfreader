import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_create_kafka_producer(mocker):
    return mocker.patch('pdf_reader.kafka_producer.create_kafka_producer', autospec=True)


def test_upload_pdf_file(mock_create_kafka_producer, monkeypatch):
    monkeypatch.setenv("BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("PDF_TEXT_TOPIC", "pdf-text")

    from pdf_reader.main import app

    mock_producer = Mock()
    mock_create_kafka_producer.return_value = mock_producer

    client = TestClient(app)

    pdf_contents = open('tests/sample.pdf', 'rb').read()

    response = client.post(
        "/api/reader",
        data={"id": "123"},
        files={"file": ("sample.pdf", pdf_contents, "application/pdf")}
    )

    assert response.status_code == 200
    assert response.json() == {"file_id": "123"}
    

def test_upload_docx_file(mock_create_kafka_producer, monkeypatch):
    monkeypatch.setenv("BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("PDF_TEXT_TOPIC", "pdf-text")

    from pdf_reader.main import app

    mock_producer = Mock()
    mock_create_kafka_producer.return_value = mock_producer

    client = TestClient(app)

    docx_contents = open('tests/sample.docx', 'rb').read()

    response = client.post(
        "/api/reader",
        data={"id": "123"},
        files={"file": ("sample.docx", docx_contents, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )

    assert response.status_code == 200
    assert response.json() == {"file_id": "123"}


def test_upload_bad_file(monkeypatch):
    monkeypatch.setenv("BOOTSTRAP_SERVERS", "localhost:9092")
    monkeypatch.setenv("PDF_TEXT_TOPIC", "pdf-text")

    from pdf_reader.main import app

    client = TestClient(app)

    response = client.post(
        "/api/reader",
        data={"id": "123"},
        files={"file": ("sample.txt", b"Hello World", "text/plain")}
    )

    assert response.status_code == 400
    assert response.json() == {"message": "File type not supported"}
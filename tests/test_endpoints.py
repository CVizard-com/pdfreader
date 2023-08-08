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
        files={"pdf_file": ("sample.pdf", pdf_contents, "application/pdf")}
    )

    assert response.status_code == 200
    assert response.json() == {"file_id": "123"}
    mock_producer.send.assert_called_once()

from fastapi.testclient import TestClient
from app.api.endpoints import documents

client = TestClient(documents.router)


def test_read_document():
    response = client.get("/document/1")
    assert response.status_code == 200
    assert response.json() == {
        "doc_id": 1,
        "authors": ["string"],
        "title": "string",
        "summary": "string",
        "publisher": "string",
        "url": "string",
        "tags": ["string"],
    }


# def test_read_inexistent_document():
#     response = client.get("/document/1000")
#     assert response.status_code == 404
    # assert response.json() == {"detail": "document not found"}

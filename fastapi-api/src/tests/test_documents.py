import pytest
from fastapi.testclient import TestClient
from app.routers import documents

TEST_JSON = {
    "doc_id": 12,
    "doi": "10.7589/2018-07-182",
    "title": "Identification of Pantropic Canine Coronavirus in a Wolf (Canis lupus italicus) in Italy",
    "abstract": "We report a case in an Italian wolf (Canis lupus italicus) of pantropic canine coronavirus infection, which has previously been detected only in dogs. The wolf was coinfected by canine parvovirus type 2b and canine adenovirus type 2, which highlighted the crucial role of epidemiologic surveys in European wild carnivores.",
    "publication_year": 2019,
    "publisher": "The Journal of Wildlife Diseases",
    "url": "https://bioone.org/journals/journal-of-wildlife-diseases/volume-55/issue-2/2018-07-182/Identification-of-Pantropic-Canine-Coronavirus-in-a-Wolf-Canis-lupus/10.7589/2018-07-182.full",
    "scientific_fields": ["Medecine", "Biology"],
    "tags": ["string", "SPORT"],
    "authors": [
        {"name": "Kyle K Dickinson", "ids": ["88764984"]},
        {"name": "Leah C Hammond", "ids": ["39777352"]},
        {"name": "Courtney M Karner", "ids": ["4880657"]},
    ],
    "related_taxons": [{"gbif_id": 1, "canonical_name": "test", "rank": "class"}],
}

client = TestClient(documents.router)


def test_read_document():
    response = client.get("/document/12")
    assert response.status_code == 200
    assert response.json() == TEST_JSON


def test_read_inexistent_document():
    with pytest.raises(Exception) as e:
        response = client.get("/document/100000000000000")

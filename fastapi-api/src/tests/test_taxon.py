import pytest
from fastapi.testclient import TestClient
from app.routers import taxons

TEST_JSON = {"gbif_id": 15, "canonical_name": "test", "rank": "class"}

TEST_JSON_0 = {
    "gbif_id": 0,
    "canonical_name": "Canis Lupus Familiaris",
    "rank": "subspecies",
}


client = TestClient(taxons.router)


def test_read_taxon():
    response = client.get(
        "/taxon/0",
    )
    assert response.status_code == 200
    assert response.json() == TEST_JSON_0


def test_post_taxon():
    response = client.post("/taxon", json=TEST_JSON)
    assert response.status_code == 200
    assert response.json() == TEST_JSON


def test_existing_species():
    with pytest.raises(Exception) as e:
        response = client.post("/taxon", json=TEST_JSON_0)
        assert response.status_code == 409
        assert response.json() == {"msg": "species already exists"}

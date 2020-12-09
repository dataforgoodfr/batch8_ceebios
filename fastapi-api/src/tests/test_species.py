import pytest
from fastapi.testclient import TestClient
from app.routers import species

TEST_JSON = {
    "gbif_id": 40,
    "scientific_name": "Canis lupus familiaris",
    "canonical_name": "Canis lupus familiaris",
    "vernacular_name": "dog",
    "sub_species": "Canis lupus familiaris",
    "species": "Canis lupus",
    "genus": "Canis",
    "family": "Canidae",
    "order": "Carnivora",
    "class": "Mammalia",
    "phylum": "Chordata",
    "kingdom": "Animalia",
    "related_documents": [0],
}


client = TestClient(species.router)


def test_read_species():
    response = client.get(
        "/specy/0",
    )
    assert response.status_code == 200


def test_post_species():
    response = client.post("/specy/", json=TEST_JSON)
    assert response.status_code == 307

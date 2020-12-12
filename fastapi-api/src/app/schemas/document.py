from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from .taxon import Taxon


class Author(BaseModel):
    name: str = Field(..., example="Kyle K Dickinson")
    ids: List[str] = Field(..., example=["88764984"])


class Document(BaseModel):
    _id: ObjectId
    _inserted_at: datetime = Field(default_factory=datetime.utcnow)
    doc_id: int
    doi: str
    title: str
    abstract: str
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    url: Optional[str] = None
    scientific_fields: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    authors: Optional[List[Author]] = []
    _content: Dict
    related_taxons: List[Taxon] = []

    class Config:
        schema_extra = {
            "example": {
                "doc_id": 0,
                "doi": "10.7589/2018-07-182",
                "title": "Identification of Pantropic Canine Coronavirus in a Wolf (Canis lupus italicus) in Italy",
                "abstract": "We report a case in an Italian wolf (Canis lupus italicus) of pantropic canine coronavirus infection, which has previously been detected only in dogs. The wolf was coinfected by canine parvovirus type 2b and canine adenovirus type 2, which highlighted the crucial role of epidemiologic surveys in European wild carnivores.",
                "publication_year": 2019,
                "publisher": "The Journal of Wildlife Diseases",
                "url": "https://bioone.org/journals/journal-of-wildlife-diseases/volume-55/issue-2/2018-07-182/Identification-of-Pantropic-Canine-Coronavirus-in-a-Wolf-Canis-lupus/10.7589/2018-07-182.full",
                "scientific_fields": ["Medecine", "Biology"],
                "tags": ["string"],
                "authors": [
                    {"name": "Kyle K Dickinson", "ids": ["88764984"]},
                    {"name": "Leah C Hammond", "ids": ["39777352"]},
                    {"name": "Courtney M Karner", "ids": ["4880657"]},
                ],
                "related_taxons": [
                    {"gbif_id": 1, "rank": "class", "canonical_name": "test"}
                ],
            }
        }

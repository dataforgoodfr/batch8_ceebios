from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class Document(BaseModel):
    _id: ObjectId
    doc_id: int
    doi: str
    title: str
    abstract: str
    publication_year: Optional[int] = None
    _inserted_at: datetime = Field(default_factory=datetime.utcnow)
    publisher: Optional[str] = []
    url: Optional[str] = None
    scientific_fields: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    authors: Optional[List[str]] = []
    content: Dict
    related_species: Optional[List[int]] = []

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
                    "Flora Alfano",
                    "Giulia Dowgier",
                    "Maria Paola Valentino",
                    "Giorgio Galiero",
                    "Antonella Tinelli",
                    "Decaro Nicola",
                    "Giovanna Fusco",
                ],
                "content": {},
                "related_species": [0],
            }
        }

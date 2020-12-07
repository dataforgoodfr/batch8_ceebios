from typing import List, Optional, Dict
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from bson import ObjectId


class Document(BaseModel):
    _id: ObjectId
    doc_id: int
    doi: str = Field(None, example="10.7589/2018-07-182")
    title: str = Field(
        ...,
        example="Identification of Pantropic Canine Coronavirus in a Wolf (Canis lupus italicus) in Italy",
    )
    abstract: str = Field(
        ...,
        example="We report a case in an Italian wolf (Canis lupus italicus) of pantropic canine coronavirus infection, which has previously been detected only in dogs. The wolf was coinfected by canine parvovirus type 2b and canine adenovirus type 2, which highlighted the crucial role of epidemiologic surveys in European wild carnivores.",
    )
    publication_year: Optional[int] = Field(None, example=2019)
    # inserted_at: datetime = Field(default_factory=datetime.utcnow)
    publisher: Optional[str] = Field(..., example="The Journal of Wildlife Diseases")
    url: Optional[str] = Field(
        None,
        example="https://bioone.org/journals/journal-of-wildlife-diseases/volume-55/issue-2/2018-07-182/Identification-of-Pantropic-Canine-Coronavirus-in-a-Wolf-Canis-lupus/10.7589/2018-07-182.full",
    )
    scientific_fields: Optional[List[str]] = Field(
        None, example=["Medecine", "Biology"]
    )
    tags: Optional[List[str]] = None

    authors: Optional[List[str]] = Field(
        None,
        example=[
            "Flora Alfano",
            "Giulia Dowgier",
            "Maria Paola Valentino",
            "Giorgio Galiero",
            "Antonella Tinelli",
            "Decaro Nicola",
            "Giovanna Fusco",
        ],
    )
    content: Dict
    related_species: Optional[List[int]] = None

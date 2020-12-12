from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from bson import ObjectId


def normalize(name: str) -> str:
    return " ".join(name.split(" "))


class Specy(BaseModel):
    _id: ObjectId
    _inserted_at: datetime = Field(default_factory=datetime.utcnow)
    gbif_id: int
    scientific_name: str = Field(..., example="Canis lupus familiaris")
    canonical_name: str = Field(..., example="Canis lupus familiaris")
    vernacular_name: str = Field(None, example="dog")
    sub_species: str = Field(..., example="Canis lupus familiaris")
    species: str = Field(..., example="Canis lupus")
    genus: str = Field(..., example="Canis")
    family: str = Field(..., example="Canidae")
    order: str = Field(..., example="Carnivora")
    taxonimic_class: str = Field(..., example="Mammalia", alias="class")
    phylum: str = Field(..., example="Chordata")
    kingdom: str = Field(..., example="Animalia")

    @validator("scientific_name")
    def normalize_name(cls, v):
        assert v != "", "Empty strings are not allowed."
        return normalize(v)

    # references
    # related_documents: Optional[List[int]] = None

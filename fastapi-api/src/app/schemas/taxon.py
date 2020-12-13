from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class RankEnum(str, Enum):
    sub_species = "subspecies"
    species = "species"
    genus = "genus"
    family = "family"
    order = "order"
    taxononomic_class = "class"
    phylum = "phylum"
    kingdom = "kingdom"


def normalize(name: str) -> str:
    return " ".join(name.split(" "))


class Taxon(BaseModel):
    _id: ObjectId
    _inserted_at: datetime = Field(default_factory=datetime.utcnow)
    gbif_id: int
    canonical_name: Optional[str] = Field(None, example="Canis Lupus Familiaris")
    rank: RankEnum = Field(..., example="species")

    class Config:
        use_enum_values = True

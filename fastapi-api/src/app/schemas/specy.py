from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class Specy(BaseModel):
    _id: ObjectId
    gbif_id: int
    scientific_name: str
    related_documents: Optional[List[int]] = None

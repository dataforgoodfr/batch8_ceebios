from typing import List, Optional
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
import uuid
from bson import ObjectId


class Document(BaseModel):
    _id: ObjectId
    doc_id: int
    authors: Optional[List[str]] = None
    title: str
    summary: str
    # published_at : datetime
    # updated_at : datetime = Field(default_factory=datetime.utcnow)
    publisher: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None

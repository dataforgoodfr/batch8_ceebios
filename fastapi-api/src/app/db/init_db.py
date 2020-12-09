from .db import db


async def init_db():
    # creating indexes for text search
    db.documents.create_index([("abstract", "text"), ("title", "text")])
    db.species.create_index([("scientific_name", "text")])

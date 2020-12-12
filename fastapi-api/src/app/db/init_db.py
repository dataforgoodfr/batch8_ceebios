from .db import db


async def init_db():
    # creating indexes for text search
    db.documents.create_index([("abstract", "text"), ("title", "text")])
    db.taxons.create_index([("canonical_name", "text")])

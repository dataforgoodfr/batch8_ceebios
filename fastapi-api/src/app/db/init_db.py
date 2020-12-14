from .db import db


async def init_db():
    # indexing ids
    db.documents.create_index("doc_id", unique=True)
    db.taxons.create_index("gbif_id", unique=True)
    # creating indexes for text search
    db.documents.create_index([("abstract", "text"), ("title", "text")])
    db.taxons.create_index([("canonical_name", "text")])

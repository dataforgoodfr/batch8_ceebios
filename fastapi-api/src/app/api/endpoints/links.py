from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.db.db import db

router = APIRouter()


@router.put("/link/{doc_id}/{gbif_id}", response_model=schemas.Document)
async def link_document_to_specy(gbif_id: int, doc_id: int):
    document = await db.documents.find_one({"doc_id": doc_id})
    if document is None:
        raise HTTPException(
            status_code=404, detail=f"document id:{doc_id} does not exists"
        )
    specy = await db.species.find_one({"gbif_id": gbif_id})
    if specy is None:
        raise HTTPException(
            status_code=404, detail=f"specy id:{gbif_id} does not exists"
        )
    if gbif_id not in document["related_species"]:
        document["related_species"] += [gbif_id]
        db.document.update_one(
            {"doc_id": doc_id},
            {"$set": {"related_species": document["related_species"]}},
        )
        return document
    else:
        raise HTTPException(status_code=404, detail=f"reference already exists")

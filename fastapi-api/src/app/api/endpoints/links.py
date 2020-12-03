from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.db.db import db

router = APIRouter()


@router.put("/link/{doc_id}/{gbif_id}", response_model=schemas.Specy)
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
    if doc_id not in specy["related_documents"]:
        specy["related_documents"] += [doc_id]
        db.species.update_one(
            {"gbif_id": gbif_id},
            {"$set": {"related_documents": specy["related_documents"]}},
        )
        return specy
    else:
        raise HTTPException(status_code=404, detail=f"link between already exists")

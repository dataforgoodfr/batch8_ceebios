from app import schemas
from app.db.db import db
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.put("/add_reference/{doc_id}/{gbif_id}", response_model=schemas.Document)
async def link_document_to_specy(gbif_id: int, doc_id: int):
    document = await db.documents.find_one({"doc_id": doc_id})
    if document is None:
        raise HTTPException(
            status_code=404, detail=f"document id:{doc_id} does not exists"
        )
    taxon = await db.taxons.find_one({"gbif_id": gbif_id}, {"_id": False})
    if taxon is None:
        raise HTTPException(
            status_code=404, detail=f"specy id:{gbif_id} does not exists"
        )
    if taxon not in document["related_taxons"]:
        document["related_taxons"] += [taxon]
        await db.documents.update_one(
            {"doc_id": doc_id},
            {"$set": {"related_taxons": document["related_taxons"]}},
        )
        return document
    else:
        raise HTTPException(status_code=404, detail="reference already exists")

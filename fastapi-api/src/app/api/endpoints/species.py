from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.db.db import db

router = APIRouter()


@router.get("/specy/{gbif_id}", response_model=schemas.Specy)
async def read_specy(gbif_id: int):
    specy = await db.species.find_one({"gbif_id": gbif_id})
    print(specy)
    if specy:
        return specy
    else:
        raise HTTPException(status_code=404, detail=f"specy not found")


@router.post("/specy")
async def create_specy(specy: schemas.Specy):
    json_compatible_specy_data = jsonable_encoder(specy)
    specy_in_db = await db.species.find_one({"gbif_id": specy.gbif_id})
    if specy_in_db:
        raise HTTPException(status_code=404, detail=f"specy already exists")
    await db.species.insert_one(json_compatible_specy_data)
    return specy


@router.get("/specy/{gbif_id}/related_documents", response_model=List[schemas.Document])
async def related_documents(gbif_id: int):
    specy = await db.species.find_one({"gbif_id": gbif_id})
    if specy is None:
        raise HTTPException(status_code=404, detail=f"specy not found")
    related_doc_ids = specy.get("related_documents")
    if related_doc_ids is None:
        raise HTTPException(status_code=404, detail=f"no related document found")
    cursor = db.documents.find({"doc_id": {"$in": related_doc_ids}})
    related_documents = []
    for doc in await cursor.to_list(length=100):
        related_documents.append(doc)
    return related_documents

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.db.db import db

router = APIRouter()


@router.get("/species", response_model=List[schemas.Specy])
async def read_documents(skip: int = 0, limit: int = 10):
    species = []
    cursor = db.species.find().skip(skip).limit(limit)
    for specy in await cursor.to_list(length=100):
        species.append(specy)
    return species


@router.get("/specy/{gbif_id}", response_model=schemas.Specy)
async def read_specy(gbif_id: int):
    specy = await db.species.find_one({"gbif_id": gbif_id})
    if specy:
        return specy
    else:
        raise HTTPException(status_code=404, detail=f"specy not found")


@router.post("/specy")
async def create_specy(specy: schemas.Specy):
    specy_in_db = await db.species.find_one({"gbif_id": specy.gbif_id})
    if specy_in_db:
        raise HTTPException(status_code=409, detail=f"specy already exists")
    json_compatible_specy_data = jsonable_encoder(specy)
    await db.species.insert_one(json_compatible_specy_data)
    return specy


@router.get("/specy/{gbif_id}/related_documents", response_model=List[schemas.Document])
async def get_related_documents(gbif_id: int):
    specy = await db.species.find_one({"gbif_id": gbif_id})
    if specy is None:
        raise HTTPException(status_code=404, detail=f"specy not found")
    cursor = db.documents.find({"related_species": gbif_id})
    related_documents = []
    for doc in await cursor.to_list(length=100):
        related_documents.append(doc)
    return related_documents

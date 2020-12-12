from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.db.db import db

router = APIRouter()


@router.get("/taxons", response_model=List[schemas.Taxon])
async def read_taxons(skip: int = 0, limit: int = 10):
    taxons = []
    cursor = db.taxons.find().skip(skip).limit(limit)
    for taxon in await cursor.to_list(length=100):
        taxons.append(taxon)
    return taxons


@router.get("/taxon/search/{query}", response_model=List[schemas.Taxon])
async def text_search_taxon(query: str):
    taxons = []
    cursor = db.taxons.find({"$text": {"$search": query}}).collation(
        {"locale": "en", "strength": 2}
    )
    for taxon in await cursor.to_list(length=100):
        taxons.append(taxon)
    return taxons


@router.get("/taxon/{gbif_id}", response_model=schemas.Taxon)
async def read_taxon(gbif_id: int):
    taxon = await db.taxons.find_one({"gbif_id": gbif_id})
    if taxon:
        return taxon
    else:
        raise HTTPException(status_code=404, detail="taxon not found")


@router.post("/taxon")
async def create_taxon(taxon: schemas.Taxon):
    taxon_in_db = await db.taxons.find_one({"gbif_id": taxon.gbif_id})
    if taxon_in_db:
        raise HTTPException(status_code=409, detail="taxon already exists")
    json_compatible_taxon_data = jsonable_encoder(taxon)
    await db.taxons.insert_one(json_compatible_taxon_data)
    return taxon


@router.get("/taxon/{gbif_id}/related_documents", response_model=List[schemas.Document])
async def get_related_documents(gbif_id: int):
    taxon = await db.taxons.find_one({"gbif_id": gbif_id})
    if taxon is None:
        raise HTTPException(status_code=404, detail="species not found")
    cursor = db.documents.find({"related_taxons.gbif_id": gbif_id})
    related_documents = []
    for doc in await cursor.to_list(length=100):
        related_documents.append(doc)
    return related_documents

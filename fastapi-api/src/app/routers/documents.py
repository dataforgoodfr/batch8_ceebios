from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app import schemas
from typing import List
from app.db.db import db

router = APIRouter()


@router.get("/documents", response_model=List[schemas.Document])
async def read_documents(skip: int = 0, limit: int = 10):
    documents = []
    cursor = db.documents.find().skip(skip).limit(limit)
    for doc in await cursor.to_list(length=100):
        documents.append(doc)
    return documents


@router.get("/documents/search/{query}", response_model=List[schemas.Document])
async def text_search_documents(query: str):
    documents = []
    cursor = db.documents.find({"$text": {"$search": query}})
    for doc in await cursor.to_list(length=100):
        documents.append(doc)
    return documents


@router.get("/document/{doc_id}", response_model=schemas.Document)
async def read_document(doc_id: int):
    document = await db.documents.find_one({"doc_id": doc_id})
    print(document)
    if document is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return document


@router.post("/document", response_model=schemas.Document)
async def create_document(document: schemas.Document):
    document_in_db = await db.documents.find_one({"doc_id": document.doc_id})
    if document_in_db:
        raise HTTPException(status_code=409, detail="document already exists")
    json_compatible_document_data = jsonable_encoder(document)
    await db.documents.insert_one(json_compatible_document_data)
    return document


@router.get("/document/tag/{tag}", response_model=List[schemas.Document])
async def search_documents_by_tag(tag: str):
    documents = []
    cursor = db.documents.find({"tags": tag})
    for doc in await cursor.to_list(length=100):
        documents.append(doc)
    return documents


@router.put("/document/add-tag/{doc_id}/{tag}", response_model=schemas.Document)
async def add_tag_to_document(doc_id: int, tag: str):
    document = await db.documents.find_one({"doc_id": doc_id})
    if document is None:
        raise HTTPException(
            status_code=404, detail=f"document id:{doc_id} does not exists"
        )
    related_tags = document.get("tags")
    if tag in related_tags:
        return document
    else:
        document["tags"] += [tag]
        db.documents.update_one(
            {"doc_id": doc_id}, {"$set": {"tags": document["tags"]}}
        )
        return document

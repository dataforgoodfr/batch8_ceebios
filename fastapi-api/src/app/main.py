from app.config import settings
from app.db import db
from app.db.init_db import init_db
from app.routers import documents, links, taxons
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "documents",
        "description": "Operations with documents",
        "externalDocs": {
            "description": "original data",
            "url": "https://www.semanticscholar.org/",
        },
    },
    {
        "name": "taxons",
        "description": "Operations with taxons",
        "externalDocs": {
            "description": "original data",
            "url": "https://www.gbif.org/developer/species",
        },
    },
    {
        "name": "references",
        "description": "Link a document to a taxon",
    },
]
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
)


@app.on_event("startup")
async def startup():
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await db.close()


app.include_router(documents.router, tags=["documents"])
app.include_router(links.router, tags=["references"])
app.include_router(taxons.router, tags=["taxons"])


@app.get("/")
def index():
    return {"msg": "Hello World"}

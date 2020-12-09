from fastapi import FastAPI
from app.routers import documents, species, links
from app.config import settings
from app.db.init_db import init_db
from app.db import db

tags_metadata = [
    {
        "name": "documents",
        "description": "Operations with documents",
    },
    {
        "name": "species",
        "description": "Operations with species",
        "externalDocs": {
            "description": "original data",
            "url": "https://www.gbif.org/developer/species",
        },
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
    db.close()


app.include_router(documents.router, tags=["documents"])
app.include_router(species.router, tags=["species"])
app.include_router(links.router, tags=["references"])


@app.get("/")
def index():
    return {"msg": "Hello World"}

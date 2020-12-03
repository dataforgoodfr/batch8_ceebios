from fastapi import FastAPI
from app.api.endpoints import documents, species, links
from fastapi.testclient import TestClient

app = FastAPI(
    title="TreeOfLife API",
    description="Open source API to explore biodiversity knowledge graph",
)


app.include_router(documents.router, tags=["documents"])
app.include_router(species.router, tags=["species"])
app.include_router(links.router, tags=["references"])


@app.get("/")
def index():
    return {"msg": "Hello World"}

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URI)
db = client[settings.DATABASE_NAME]

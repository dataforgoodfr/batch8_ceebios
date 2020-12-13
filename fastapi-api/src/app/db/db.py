from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.DATABASE_URI)
db = client[settings.DATABASE_NAME]

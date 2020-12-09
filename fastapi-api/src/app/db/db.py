from motor import motor_asyncio
from app.config import settings

print(settings.DATABASE_URI)
print(settings.DATABASE_NAME)

client = motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URI)
db = client[settings.DATABASE_NAME]

# engine = AIOEngine(motor_client=client, database=DATABASE_NAME)

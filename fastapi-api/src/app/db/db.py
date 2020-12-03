import os
from motor import motor_asyncio
from dotenv import load_dotenv

DATABASE_URI = os.getenv('DATABASE_URI')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

client = motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[str(COLLECTION_NAME)]
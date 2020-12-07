import os
from motor import motor_asyncio
from dotenv import load_dotenv
from odmantic import AIOEngine

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]

# engine = AIOEngine(motor_client=client, database=DATABASE_NAME)


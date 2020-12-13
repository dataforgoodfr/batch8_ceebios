import json
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_UNSERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

client = MongoClient(
    f"mongodb://{MONGO_UNSERNAME}:{MONGO_PASSWORD}@165.22.121.95:27017/"
)

db = client.documents
print(db)

posts = db.posts

for file in os.listdir("/Volumes/Extreme SSD/ceebios"):
    if file.endswith(".json"):
        with open(os.path.join("/Volumes/Extreme SSD/ceebios", file)) as json_file:
            new_posts = json.load(json_file)
    result = posts.insert_many(new_posts)
    print("Number of inserted articles: ")
    print(len(result.inserted_ids))
    print(f"done with {file}")

running_sum = 0
for post in posts.find():
    running_sum += 1
print(running_sum)

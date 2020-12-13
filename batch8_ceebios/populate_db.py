import json
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = 27017
MONGO_dbname = 'ceebios'
MONGO_UNSERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=MONGO_UNSERNAME,  password=MONGO_PASSWORD)
db1 = client[MONGO_dbname]

# now you have one cursor for collection species, and a second for documents

cursor_species = db1['species']
cursor_documents = db1['documents']

print('- cursors to write or find into Mongodb:')
print('cursor_species', cursor_species)
print('cursor_documents', cursor_documents)

db = client.documents
print(db)


posts = db.posts # ? ? i don't understand i don't see such collection

for file in os.listdir("/Volumes/Extreme SSD/ceebios"):
    if file.endswith(".json"):
        with open(os.path.join("/Volumes/Extreme SSD/ceebios", file)) as json_file:
            new_posts = json.load(json_file)

            
            # result = posts.insert_many(new_posts)
            # logiquement on insert ici l'article 
            result = cursor_documents.insert_many(new_posts)
    
    print("Number of inserted articles: ")
    print(len(result.inserted_ids))
    print(f"done with {file}")

running_sum = 0
for post in posts.find():
    running_sum += 1
print(running_sum)

# fermeture 
client.close()

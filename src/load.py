from sentence_transformers import SentenceTransformer
import json
from pymongo import MongoClient

model = SentenceTransformer("all-MiniLM-L6-v2")
client = MongoClient("mongodb://localhost:27017/")
db = client["constitution_db"]
collection = db["vectors"]

with open("constitution_clean.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

for article in articles:
    vector = model.encode(article["text"]).tolist()
    collection.insert_one({"article": article["article"], "text": article["text"], "vector": vector})

print("Data successfully loaded into MongoDB!")

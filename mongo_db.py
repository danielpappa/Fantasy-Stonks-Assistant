import pymongo
import os
import news_scraper

def get_mongo_client(mongo_uri):
    try:
        client = pymongo.MongoClient(mongo_uri)
        print("Connection to MongoDB successful")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None

mongo_uri = os.getenv('MONGO_URI')

if not mongo_uri:
    print("MONGO_URI not set in environment variables")

mongo_client = get_mongo_client(mongo_uri)

db = mongo_client["fantasy"]
collection = db["news"]

df = news_scraper.get_df()

collection.delete_many({})
documents = df.to_dict("records")
collection.insert_many(documents)
print("Insertion worked out")

def get_collection():
    return collection
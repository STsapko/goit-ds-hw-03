import pymongo
from pymongo import MongoClient # type: ignore
from bson.objectid import ObjectId # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение строки подключения из .env
MONGO_URI = os.getenv("MONGO_URI")

# Подключение к MongoDB
client = MongoClient(MONGO_URI)
db = client['cats_db']
collection = db['cats']

def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    collection.insert_one(cat)
    print(f"{name} added")

def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)

def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"{name} not found")

def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count > 0:
        print(f"{name}'s age update to {new_age}")
    else:
        print(f"{name} not found")

def add_cat_feature(name, new_feature):
    result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
    if result.matched_count > 0:
        print(f"'{new_feature}' added to {name}")
    else:
        print(f"{name} not found")

def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"{name} deleted")
    else:
        print(f"{name} not found")

def delete_all_cats():
    result = collection.delete_many({})
    print(f"{result.deleted_count} deleted")

if __name__ == "__main__":
    try:
        create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
        read_all_cats()
        read_cat_by_name("barsik")
        update_cat_age("barsik", 4)
        add_cat_feature("barsik", "любить гратися")
        delete_cat_by_name("barsik")
        delete_all_cats()
    except pymongo.errors.PyMongoError as e:
        print(f"error {e}")

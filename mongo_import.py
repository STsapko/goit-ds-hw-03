import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение строки подключения из .env
MONGO_URI = os.getenv("MONGO_URI")

# Подключение к MongoDB
client = MongoClient(MONGO_URI)

# Создаем базу данных и коллекции
db = client["quotes_db"]
quotes_collection = db["quotes"]
authors_collection = db["authors"]

# Функция для импорта данных из JSON файла в коллекцию MongoDB
def import_data(json_file, collection):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        collection.insert_many(data)
        print(f"Данные из {json_file} успешно импортированы в коллекцию.")

if __name__ == "__main__":
    try:
        # Импорт данных в коллекцию authors
        import_data("authors.json", authors_collection)

        # Импорт данных в коллекцию quotes
        import_data("quotes.json", quotes_collection)

        print("Все данные успешно импортированы в базу данных MongoDB.")
    except Exception as e:
        print(f"Произошла ошибка при импорте данных: {e}")

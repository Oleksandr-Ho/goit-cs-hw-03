from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до бази даних
client = MongoClient(
    "mongodb+srv://goitlearn:<password>@cluster0.xd3ttcy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client.pet_database  # Створення або вибір бази даних
collection = db.cats      # Створення або вибір колекції

# Функції для CRUD операцій

def create_document(document):
    """ Створення нового документа у колекції """
    try:
        result = collection.insert_one(document)
        print(f"Document inserted with id: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_all_documents():
    """ Читання всіх документів з колекції """
    try:
        documents = collection.find()
        for doc in documents:
            print(doc)
    except Exception as e:
        print(f"An error occurred: {e}")

def read_document_by_name(name):
    """ Читання документа за іменем """
    try:
        document = collection.find_one({"name": name})
        if document:
            print(document)
        else:
            print("No document found with that name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_age_by_name(name, age):
    """ Оновлення віку кота за іменем """
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": age}})
        if result.modified_count > 0:
            print("Document updated successfully.")
        else:
            print("No document found with that name or age is the same as current.")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_feature_by_name(name, feature):
    """ Додавання нової характеристики до списку features кота за іменем """
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print("Feature added successfully.")
        else:
            print("No document found with that name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_document_by_name(name):
    """ Видалення документа за іменем """
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print("Document deleted successfully.")
        else:
            print("No document found with that name.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_all_documents():
    """ Видалення всіх документів з колекції """
    try:
        result = collection.delete_many({})
        print(f"Documents deleted count: {result.deleted_count}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Приклади використання функцій
create_document({
    "name": "barsik",
    "age": 3,
    "features": ["ходить в капці", "дає себе гладити", "рудий"]
})
create_document({
    "name": "Liza",
    "age": 5,
    "features": ["ходить в лоток", "дає себе гладити", "білий"]
})


read_all_documents()
read_document_by_name("barsik")
update_age_by_name("barsik", 4)
add_feature_by_name("barsik", "ловить мишей")
read_document_by_name("barsik")
delete_document_by_name("barsik")
delete_all_documents()

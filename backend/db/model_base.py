from backend.db.connection import MongoDBConnection

def initialize_collection(func):
    def wrapper(self, *args, **kwargs):
        db = MongoDBConnection()
        collection = db.adventures
        return func(self, collection, *args, **kwargs)
    return wrapper

class ModelBase(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name.startswith("static_"):
                attrs[attr_name] = initialize_collection(attr_value)
        return super().__new__(cls, name, bases, attrs)
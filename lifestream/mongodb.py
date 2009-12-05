from django.conf import settings

from pymongo import Connection

MONGODB_HOST = getattr(settings, "MONGODB_HOST", "localhost")
MONGODB_PORT = getattr(settings, "MONGODB_PORT", 27017)
MONGODB_DB = getattr(settings, "MONGODB_DB", "lifestream_db")
MONGODB_LS_COLLECTION = getattr(settings, "MONGODB_LIFESTREAM_COLLECTION", "lifestream")
    
_connection = Connection(MONGODB_HOST, MONGODB_PORT)
_db = _connection[MONGODB_DB]
_collection = _db[MONGODB_LS_COLLECTION]
_collection.create_index("lifestream:timestamp")
_collection.create_index("id")
_collection.create_index("lifestream:provider")
_collection.create_index("lifestream:source")

def get_collection():
    return _collection
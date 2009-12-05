from django.conf import settings

from pymongo import Connection

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "lifestream_db"
MONGODB_LS_COLLECTION = "lifestream"

if hasattr(settings, "MONGODB_HOST"):
    MONGODB_HOST = settings.MONGODB_HOST
if hasattr(settings, "MONGODB_PORT"):
    MONGODB_PORT = settings.MONGODB_PORT
if hasattr(settings, "MONGODB_DB"):
    MONGODB_DB = settings.MONGODB_DB
if hasattr(settings, "MONGODB_LIFESTREAM_COLLECTION"):
    MONGODB_LS_COLLECTION = settings.MONGODB_LS_COLLECTION
    
_connection = Connection(MONGODB_HOST, MONGODB_PORT)
_db = _connection[MONGODB_DB]
_collection = _db[MONGODB_LS_COLLECTION]
_collection.create_index("lifestream:timestamp")
_collection.create_index("id")
_collection.create_index("lifestream:provider")
_collection.create_index("lifestream:source")

def get_collection():
    return _collection
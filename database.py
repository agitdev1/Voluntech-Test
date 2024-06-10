# MongoDB connection
from pymongo import MongoClient

client = MongoClient("")
db = client.db_voluntech
volunteer_collection = db.volunteer
organization_collection = db.organization
sessions_collection = db.sessions
tokens_collection = db.reset_tokens
opportunities_collection = db.opportunities

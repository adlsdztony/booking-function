import pymongo


import os

MONGO_LINK = os.environ.get('MONGO_LINK')

db = pymongo.MongoClient(MONGO_LINK).booking

users = db.user
log = db.log
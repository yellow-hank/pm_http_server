from flask_pymongo import PyMongo

def connect_to_db(app):
    mongo = PyMongo(app)
    if mongo:
        print('Connected to mongo')
    else:
        print('Failed connecting to mongo')
    return mongo

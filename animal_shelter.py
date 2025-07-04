from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self,username,password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        #USER = 'briannahrhea'
        #PASS = 'SNHUCS499Mongo1!'
        #HOST = 'mongodb+srv://briannahrhea:<db_password>@cluster0.h1z4brd.mongodb.net/'
        #PORT = 27017
        #DB = 'AAC'
        #COL = 'animals'
        #
        # Initialize Connection
        #
        uri = f"mongodb+srv://{username}:{password}@cluster0.h1z4brd.mongodb.net/"
        self.client = MongoClient(uri)
        self.database = self.client["AAC"]
        self.collection = self.database["animals"]

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            result = self.collection.insert_one(data)
            return result.acknowledged
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Create method to implement the R in CRUD.
    def read(self, data):
        if data is not None:
            result = self.collection.find(data, { '_id': 0} )
            return list(result)
        else:
            raise Exception("Search query is empty")
            
# Create method to implement the U in CRUD
    def update(self, data, change):
        if data is not None and change is not None:
            update_result = self.collection.update_many(data, {"$set": change})
            return update_result.modified_count
        else:
            raise Exception("Nothing to update, because data parameter is empty")
            
# Create method to implement the D in CRUD
    def delete(self, data):
        if data is not None:
            delete_result = self.collection.delete_many(data)
            return delete_result.deleted_count
        else:
            raise Exception("Nothing to delete, because data parameter is empty")
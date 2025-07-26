from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        uri = f"mongodb+srv://{username}:{password}@cluster0.h1z4brd.mongodb.net/"
        self.client = MongoClient(uri)
        self.database = self.client["AAC"]
        self.collection = self.database["animals"]

    # ========== CREATE ==========
    def create(self, data):
        if isinstance(data, dict):
            result = self.collection.insert_one(data)
            return result.acknowledged
        else:
            raise Exception("Data must be a dictionary.")

    # ========== READ ==========
    def read(self, data):
        if data is not None:
            result = self.collection.find(data, {'_id': 0})
            return list(result)
        else:
            raise Exception("Search query is empty")

    # ========== UPDATE ==========
    def update(self, data, change):
        if data and change:
            update_result = self.collection.update_many(data, {"$set": change})
            return update_result.modified_count
        else:
            raise Exception("Invalid update request.")

    # ========== DELETE ==========
    def delete(self, data):
        if data:
            delete_result = self.collection.delete_many(data)
            return delete_result.deleted_count
        else:
            raise Exception("Nothing to delete.")

    # ========== SAVE BOOKMARK ==========
    def save_bookmark(self, animal_id, user_id='default_user'):
        self.database['bookmarks'].insert_one({'user_id': user_id, 'animal_id': animal_id})

    # ========== RETRIEVE BOOKMARK ==========
    def get_bookmarks(self, user_id='default_user'):
        bookmarks = list(self.database['bookmarks'].find({'user_id': user_id}))
        animal_ids = [b['animal_id'] for b in bookmarks]
        return list(self.collection.find({'animal_id': {'$in': animal_ids}}, {'_id': 0}))

    # ========== REMOVE BOOKMARK ==========
    def remove_bookmark(self, animal_id, user_id='default_user'):
        self.database['bookmarks'].delete_one({'user_id': user_id, 'animal_id': animal_id})

    # ========== CLEAR BOOKMARK ==========
    def clear_all_bookmarks(self, user_id='default_user'):
        self.database['bookmarks'].delete_many({'user_id': user_id})
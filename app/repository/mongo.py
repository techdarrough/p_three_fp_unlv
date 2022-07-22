import os
from pymongo import MongoClient

COLLECTION_NAME = 'projects'


class MogoRepository(object):
    def __init__(self):
        mongo_url = os.environ.get('MONGO_URL')
        self.db = MongoClient(mongo_url).projects

    def find_all(self, selector):
        return self.db.projects.find(selector)
    
    def find(self, selector):
        return self.db.projects.find_one(selector)
 
    def create(self, project):
        return self.db.projects.insert_one(project)

    def update(self, selector, project):
        return self.db.projects.replace_one(selector, project).modified_count
    
    def delete(self, selector):
        return self.db.projects.delete_one(selector).deleted_count

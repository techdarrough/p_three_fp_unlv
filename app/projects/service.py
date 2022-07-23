from ..repository import Repository
from ..repository.mongo import MongoRepository
from .schema import ProjectSchema

# define a service class that can tranlaste the data from the incoming payload
# represented by GitHubSchema model(class...model class...class model)

class Service(object):
    def __init__(self, user_id, repo_client=Repository(adapter=MongoRepository)):
        self.repo_client = repo_client
        self.user_id = user_id 

        if not user_id:
            raise Exception("Denied! No user ID has been provided!")

    # call methods created in mongo.py find_all find create detele 
    def find_all_projects(self):
        projects = self.repo_client.find_all({'user_id': self.user_id})
        return [self.dump(project) for project in projects]
    
    def find_project(self, repo_id):
        project = self.repo_client.find({'user_id': self.user_id, 'repo_id': repo_id})
        return self.dump(project)
    # use helper function to prep githubrepo data 
    def create_project_for(self, githubRepo):
        self.repo_client.create(self.prepare_project(githubRepo))
        return self.dump(githubRepo.data)
    
    def udpate_project_with(self, repo_id, githubRepo):
        records_affected = self.repo_client.update({'user_id': self.user_id, 'repo_id': repo_id}, self.prepare_project(githubRepo))
        return records_affected > 0
    
    def dump(self, data):
        return ProjectSchema(exclude=['_id']).dump(data).data
    #helper function to prep set user and data payload then returns it to the function
    def prepare_project(self, githubRepo):
        data = githubRepo.data
        data['user_id'] = self.user_id
        return data
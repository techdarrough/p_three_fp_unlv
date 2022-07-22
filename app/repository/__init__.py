# might want to use another database

# define a class to represent a respository



class Repository(object):
    def __init__(self, adapter=None):
        self.client = adapter()
    # generic routes 
    #find all take in parm selector as input finds all returns
    def find_all(self, selector):
        return self.client.find_all(selector)
    #find one then return rinse and repeat
    def find(self, selector):
        return self.client.find(selector)
    # creates new take in project as parm
    def create(self, project):
        return self.client.create(project)
    # updates existing takes selector and project as parms
    def update(self, selector, project):
        return self.client.update(selector, project)
    #deletes
    def delete(self, selector):
        return self.client.delete(selector)
    
    
    

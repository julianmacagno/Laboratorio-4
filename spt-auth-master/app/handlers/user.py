import uuid
from models.user import UserModel

class UserHandler(object):
    """ user handler for auth app """

    def __init__(self):
        self.user_model = UserModel()

    def audit(self, req): 
        data = req.json
        return self.user_model.getAuditEvents({
            "username": data
        })
        

    def register(self, req):
        data = req.json
        return self.user_model.create({
            'username': str(data['username']),
            'password': str(data['password'])
        })
    
    def login(self, req):
        data = req.json
        return self.user_model.login({
            'username': str(data['username']),
            'password': str(data['password'])
        })
    
    def logout(self, req):
        data = req.json
        print str(data['username'])
        return self.user_model.logout(str(data['username']))
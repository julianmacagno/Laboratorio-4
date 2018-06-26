from dal.user import UserDal

class UserModel(object):
    """ user model for spt-auth service """

    def __init__(self):
        self.user_dal = UserDal()
    
    def getAuditEvents(self, u):
        return self.user_dal.getAuditEvents(u)

    def create(self, u):
        if self.user_dal.insert(u):
            self.user_dal.log_on_audit_events(u['username'], "Successful Registration")
            return True
        else:
            self.user_dal.log_on_audit_events(u['username'], "Registration Error: Invalid Username")
            return False
    
    def login(self, u):
        user = self.user_dal.get(u['username'])

        if user == None:
            self.user_dal.log_on_audit_events(u['username'], "Login Error: Invalid Username")
            return False
        elif user[1] == u['username'] and user[2] == u['password']: #user[0] es el id
            self.user_dal.log_on_audit_events(user[1], 'Successful Login')
            return True
        else: 
            self.user_dal.log_on_audit_events(user[1], "Login Error: Invalid Password")
            return False

    def logout(self, username):
        self.user_dal.log_on_audit_events(username, 'Successful Logout')
        return True
# ***********************************************************************************************************************
# *                                                                                                                     *
# *   User.py                                                                                                           *
# *   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
# *   The purpose of this file is to structure User data into a class so that User information can be easily fetched    *
# *                                                                                                                     *
# ***********************************************************************************************************************

from classes.Database import Database

class User:
    def __init__(self):
        self.ID = None
        self.Username = None
        self.isAuthenticated = False

    def authenticate(self, username, password):
        db = Database()
        users = db.getUser(username, password)
        if len(users) > 0:
            self.ID = users[0][0]
            self.Username = username
            self.isAuthenticated = True
            del db
            return True
        else:
            del db
            return False

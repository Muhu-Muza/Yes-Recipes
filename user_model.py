

registered_users = {"username": []} # pylint: disable=invalid-name


class Users(object):
    def __init__(self, email, firstname, lastname, password, username=None):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.confirm_password = password

    def sign_up(self):
        if self.username and self.password:
            if self.username in registered_users:
                return 'User Already Exists!'
            else:
                if self.password is not None:
                    registered_users[self.username] = [self.firstname, self.lastname, self.username, self.email, self.password]
                    return registered_users
                else:
                    return 'Input password'
        else:
            return 'No user name given'

    def signin(self):
        if self.username in registered_users:
            if self.password == registered_users[self.username][0]:
                return 'Logged in'
            else:
                return 'Incorrect password'
        else:
            return 'You are not registered! Please sign up'
        
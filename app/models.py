from flask_login import UserMixin

class User(UserMixin):
    users = {
        '1': {'id': '1', 'name': 'Test User', 'password': 'test'},
    }

    def __init__(self, user_id, name, password):
        self.id = user_id
        self.name = name
        self.password = password

    @staticmethod
    def get(user_id):
        user = User.users.get(user_id)
        if user:
            return User(user_id=user['id'], name=user['name'], password=user['password'])
        return None

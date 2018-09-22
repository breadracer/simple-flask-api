from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'Shawn', 'abcd'),
    User(2, 'Josh', 'efgh'),
    User(3, 'Emily', 'ijkl')
]

mapUsernameToUser = {user.username: user for user in users}
mapIdToUser = {user.id: user for user in users}

def authenticate(username, password):
    user = mapUsernameToUser.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    userId = payload['identity']
    return mapIdToUser.get(userId, None)


import requests


class User:
    def __init__(self, from_dict):
        self.id = from_dict["id"]
        self.username = from_dict["username"]
        self.password = from_dict["password"]
        self.admin = from_dict["admin"]


def get_user_by_id(id):
    print("ayy", type(id), id)
    response = requests.get("http://127.0.0.1:5001/api/users/id/%(id)d" % {
        "id": id
    })
    if response.status_code == 200:
        return User(response.json())
    return None


def get_user_by_username(username):
    response = requests.get("http://127.0.0.1:5001/api/users/username/%(username)s" % {
        "username": username
    })
    if response.status_code == 200:
        return User(response.json())
    return None

import json

def hello_world():
    return {"Hello": "World"}

def get_users():
    return json.loads(open("users.json").read())
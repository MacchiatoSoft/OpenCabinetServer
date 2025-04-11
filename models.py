from uuid import uuid4
class User:

    id : str
    username : str 
    password : str

    def __init__(self, id:str, username:str, password:str):
        self.id = id
        self.username = username
        self.password = password
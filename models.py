import json
from uuid import uuid4
class User:

    id : str
    name : str 
    password : str

    def __init__(self, id:str, username:str, password:str):
        self.id = id
        self.name = username
        self.password = password

    def toJSON(self):
        return {
            "userid":self.id,
            "username":self.name,
            "password":self.password
        }
    
class DrawerPointer:

    id : str
    name : str
    type : str
    ownername : str

    def __init__(self, id:str, drawername:str, drawertype:str, ownername:str):
        self.id = id
        self.name = drawername
        self.type = drawertype
        self.ownername = ownername
    
    def toJSON(self):
        return {
            "drawerid":self.id,
            "drawername":self.name,
            "drawertype":self.type,
            "ownername":self.ownername
        }

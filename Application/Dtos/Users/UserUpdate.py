from pydantic import BaseModel








class UserUpdate(BaseModel) : 

    Id:str
    Email:str
    Password:str

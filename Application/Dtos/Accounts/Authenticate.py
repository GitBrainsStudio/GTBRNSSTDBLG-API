from pydantic import BaseModel








class Authenticate(BaseModel) : 

    Email:str
    Password:str
    
from pydantic import BaseModel








class ProjectUpdate(BaseModel) : 

    Id:str
    Title:str
    Description:str

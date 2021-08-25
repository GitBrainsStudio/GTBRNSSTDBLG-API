from typing import List
from pydantic import BaseModel








class PostUpdate(BaseModel) : 

    Id:str
    Title:str
    Content:str
    TagsTitles:List[str]
    ImagesIds:List[str]

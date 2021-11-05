from typing import List
from pydantic import BaseModel
from Domain.Entities.Tag import Tag







class PostCreate(BaseModel) : 

    Title:str
    Content:str
    TagsTitles:List[str]
    ImagesIds:List[str]
    
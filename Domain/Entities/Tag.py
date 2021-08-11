from sqlalchemy.orm import relationship
from Domain.Entities.Project import Project
from Domain.Entities.Base import Base, project_tag 
from sqlalchemy import Column, String

class Tag(Base) : 

    __tablename__ = 'tags'

    Id = Column('id', String, primary_key=True)
    Title = Column('title', String)

    def __init__(
        self,
        id:str,
        title:str
        ) -> None :
        self.Id = id
        self.Title = title

    def Update(self, title:str,) : 
        self.Title = title
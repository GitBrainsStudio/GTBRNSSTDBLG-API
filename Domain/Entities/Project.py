from sqlalchemy.orm import relationship
from Domain.Entities.Base import Base, project_tag
from sqlalchemy import Column, String





class Project(Base) : 

    __tablename__ = 'projects'

    Id = Column('id', String, primary_key=True)
    Title = Column('title', String)
    Description = Column('description', String)

    Tags = relationship(
        "Tag",
        secondary=project_tag,
        lazy="joined")
        
    def __init__(
        self,
        id:str,
        title:str,
        description:str,
        ) -> None :
        self.Id = id
        self.Title = title
        self.Description = description

    def Update(self, title:str, description:str) : 
        self.Title = title
        self.Description = description
    

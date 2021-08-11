from Domain.Entities.Tag import Tag
from typing import List
from sqlalchemy.orm import relationship
from Domain.Entities.Base import Base, post_tag
from sqlalchemy import Column, String

class Post(Base) : 

    __tablename__ = 'posts'

    Id = Column('id', String, primary_key=True)
    Title = Column('title', String)
    CreateDate = Column('create_date', String)
    Content = Column('content', String)
    UserId =  Column('user_id', String)
    Tags = relationship(
        "Tag",
        secondary=post_tag,
        lazy="joined")

    def __init__(
        self,
        id:str,
        title:str,
        content:str,
        createDate:str,
        userId:str,
        tags:List[Tag]
        ) -> None :
        self.Id = id
        self.Title = title
        self.Content = content
        self.CreateDate = createDate
        self.UserId = userId
        self.Tags = tags

    def Update(self, title:str, content:str, tags:List[Tag]) : 
        self.Title = title
        self.Content = content
        self.Tags = tags


from Domain.Entities.Image import Image
from Domain.Entities.Tag import Tag
from typing import List
from sqlalchemy.orm import relationship
from Domain.Entities.Base import Base, post_tag, post_image
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
    
    Images = relationship(
        "Image",
        secondary=post_image,
        lazy="joined")

    def __init__(
        self,
        id:str,
        title:str,
        content:str,
        createDate:str,
        userId:str,
        tags:List[Tag],
        images:List[Image]
        ) -> None :
        self.Id = id
        self.Title = title
        self.Content = content
        self.CreateDate = createDate
        self.UserId = userId
        self.Tags = tags
        self.Images = images

    def Update(self, title:str, content:str, tags:List[Tag], images:List[Image]) : 
        self.Title = title
        self.Content = content
        self.Tags = tags
        self.Images = images


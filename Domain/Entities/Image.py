from Domain.Entities.Base import Base
from sqlalchemy import Column, String

class Image(Base) : 

    __tablename__ = 'images'

    Id = Column('id', String, primary_key=True)
    Title = Column('title', String)
    UploadDate = Column('upload_date', String)
    UserId =  Column('user_id', String)

    def __init__(
        self,
        id:str,
        title:str,
        uploadDate:str,
        userId:str,
        ) -> None :
        self.Id = id
        self.Title = title
        self.UploadDate = uploadDate
        self.UserId = userId
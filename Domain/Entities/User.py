from Domain.Entities.Base import Base
from sqlalchemy import Column, String







class User(Base) : 

    __tablename__ = 'users'

    Id = Column('id', String, primary_key=True)
    Email = Column('email', String)
    RegistrationDate = Column('registration_date', String)
    Password = Column('password', String)

    def __init__(self, id:str, email:str, registrationDate:str, password:str) -> None:
        self.Id = id
        self.Email = email
        self.RegistrationDate = registrationDate
        self.Password = password
    
    def Update(self, email:str, password:str) :
         self.Email = email
         self.Password = password

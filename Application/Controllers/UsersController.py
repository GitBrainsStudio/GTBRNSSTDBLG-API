from sqlalchemy.sql.expression import false
from Application.Middlewares.TokenChecker import TokenChecker
from Infrastructure.Services.SessionService import SessionService
from Application.Service.TokenService import TokenService
from Application.Dtos.Users.UserUpdate import UserUpdate
from Application.Dtos.Users.UserDelete import UserDelete
from Application.Dtos.Users.UserCreate import UserCreate
from Domain.Entities.User import User
from Startup.FastApiService import FastApiService
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from Application.Dtos.Accounts.Authenticate import Authenticate
from Application.Dtos.Accounts.Account import Account as AccountDto
from Application.Dtos.Users.User import User as UserDto
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, HTTPException, Depends, Request
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class UsersController() : 

    _fastApiService:FastApiService
    _tokenService:TokenService
    _sessionService:SessionService

    def __init__(
        self,
        fastApiService:FastApiService,
        tokenService:TokenService,
        sessionService:SessionService) -> None:
        self._tokenService = tokenService
        self._sessionService = sessionService
        self._fastApiService = fastApiService
        # self._fastApiService._fastApi.add_api_route(path="/users", endpoint=self.GetAll, methods=["GET"], dependencies=[Depends(self._tokenService.Check)])
        # self._fastApiService._fastApi.add_api_route(path="/users/{userId}", endpoint=self.GetById, methods=["GET"])
        # self._fastApiService._fastApi.add_api_route(path="/users/", endpoint=self.Create, methods=["POST"])
        # self._fastApiService._fastApi.add_api_route(path="/users/", endpoint=self.Update, methods=["PUT"])
        # self._fastApiService._fastApi.add_api_route(path="/users/{userId}", endpoint=self.Delete, methods=["DELETE"])
        self._fastApiService._fastApi.add_api_route(path="/users/authenticate", endpoint=self.Authenticate, methods=["POST"])

    def GetById(self, userId:str) : 
        return self._sessionService.GetDBContext().query(User).filter(User.Id == userId).one()

    def GetAll(self) : 
        return self._sessionService.GetDBContext().query(User).all()

    def Update(self, userUpdate:UserUpdate) : 
        user = self._sessionService.GetDBContext().query(User).filter(User.Id == userUpdate.Id).one()
        user.Update(userUpdate.Email, userUpdate.Password)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Пользователь успешно обновлен", "id" : user.Id})

    def Create(self, userCreate:UserCreate) : 
        
        users = self._sessionService.GetDBContext().query(User).filter(User.Email == userCreate.Email).all()

        if len(users) is not 0 : 
            return JSONResponse(status_code=400, content={"message": "Пользователь с указанным почтовым адресом уже существует в системе", "email" : userCreate.Email})

        user:User = User(
            str(uuid.uuid4()),
            userCreate.Email,
             datetime.now().strftime("%m/%d/%Y"),
            userCreate.Password,
        )


        self._sessionService.GetDBContext().add(user)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Пользователь успешно добавлен", "id" : user.Id})

    def Delete(self, userDelete:UserDelete) :
        user = self._sessionService.GetDBContext().query(User).filter(User.Id == userDelete.Id).one() 
        self._sessionService.GetDBContext().delete(user)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Пользователь успешно удален"})

    def Authenticate(self, authenticateData:Authenticate) : 
        user = self._sessionService.GetDBContext().query(User).filter(User.Email == authenticateData.Email, User.Password == authenticateData.Password).one() 

        account = AccountDto()
        account.User = UserDto(user)
        account.Token = self._tokenService.GenerateToken(user)

        return account

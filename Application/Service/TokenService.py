import datetime
from Application.Service.ConfigurationService import ConfigurationService
import jwt
from Domain.Entities.User import User
import json
from starlette.requests import Request
from fastapi import HTTPException

class TokenService() : 

    _requestUserId:str
    _configurationService:ConfigurationService

    def __init__(self, configurationService:ConfigurationService) -> None:
        self._configurationService = configurationService

    def GenerateToken(self, user:User) -> str : 
        return jwt.encode({'userId': user.Id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}, self._configurationService.GetTokenSecretKey(), algorithm=self._configurationService.GetTokenAlgorithm())

    def Check(self, request: Request) :
        try:
            jwt_token = request.headers.get('authorization', None)
            payload = jwt.decode(
                jwt_token,
                key= self._configurationService.GetTokenSecretKey(),
                algorithms=[self._configurationService.GetTokenAlgorithm()]
            )
            self._requestUserId = payload['userId']
        except Exception as error:
            raise  HTTPException(status_code=401)
from Application.Service.ConfigurationService import ConfigurationService
import jwt
from Domain.Entities.User import User
import json

class TokenService() : 

    _configurationService:ConfigurationService

    def __init__(self, configurationService:ConfigurationService) -> None:
        self._configurationService = configurationService

    def GenerateToken(self, user:User) -> str : 
        return jwt.encode({'userId': user.Id }, self._configurationService.GetTokenSecretKey(), algorithm=self._configurationService.GetTokenAlgorithm())
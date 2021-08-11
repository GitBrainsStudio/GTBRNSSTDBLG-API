# sync def get_user(request):
#     return json_response({'user': str(request.user)})

# async def auth_middleware(app, handler):
#     async def middleware(request):
#         request.user = None
#         jwt_token = request.headers.get('authorization', None)
#         if jwt_token:
#             try:
#                 payload = jwt.decode(jwt_token, JWT_SECRET,
#                                      algorithms=[JWT_ALGORITHM])
#             except (jwt.DecodeError, jwt.ExpiredSignatureError):
#                 return json_response({'message': 'Token is invalid'}, status=400)

#             request.user = User.objects.get(id=payload['user_id'])
#         return await handler(request)
#     return middleware

# app = web.Application(middlewares=[auth_middleware])
# app.router.add_route('GET', '/get-user', get_user)



from starlette.requests import Request

from Application.Service.ConfigurationService import ConfigurationService
import jwt

from fastapi import HTTPException
from datetime import datetime

class TokenChecker() : 

    _configurationService:ConfigurationService
    _requestUserId:str

    def __init__(self, configurationService:ConfigurationService) -> None:
        self._configurationService = configurationService

    
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
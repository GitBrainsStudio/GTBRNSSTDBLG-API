from Application.Middlewares.TokenChecker import TokenChecker
from Application.Service.TokenService import TokenService
from Application.Controllers.UsersController import UsersController
from Infrastructure.Services.SessionService import SessionService
from Startup.UvicornService import UvicornService
from Startup.FastApiService import FastApiService
from Application.Service.ConfigurationService import ConfigurationService
from Application.Controllers.PostsController import PostsController
from Application.Controllers.ProjectController import ProjectController
from Application.Controllers.TagController import TagController






class DependenciesService() : 

    _fastApiService:FastApiService
    _configurationService:ConfigurationService
    _uvicornService:UvicornService
    _sessionService:SessionService
    _tokenService:TokenService
    _tokenChecker:TokenChecker

    def __init__(self) :
        self._fastApiService = None
        self._configurationService = None
        self._uvicornService = None
        self._sessionService = None
        self._userRepository = None
        self._postRepository = None
        self._tokenService = None
        self._tokenChecker = None

    def GetConfigurationService(self) -> ConfigurationService : 
        if not self._configurationService : 
            self._configurationService = ConfigurationService()
        return self._configurationService

    def GetFastApiService(self) -> FastApiService :
        if not self._fastApiService : 
            self._fastApiService = FastApiService(
                self.GetConfigurationService(),
                self.GetTokenChecker()
            )
        return self._fastApiService

    def GetUvicornService(self) -> UvicornService :
        if not self._uvicornService : 
            self._uvicornService = UvicornService(
                self.GetFastApiService(),
                self.GetConfigurationService()
            )
        return self._uvicornService

    def GetSessionService(self) -> SessionService : 
        if not self._sessionService : 
            self._sessionService = SessionService(
                self.GetConfigurationService()
            )
        return self._sessionService

    def GetTokenService(self) -> TokenService : 
        if not self._tokenService : 
            self._tokenService = TokenService(self.GetConfigurationService())
        return self._tokenService

    def RegisterControllers(self) : 
        UsersController(
            self.GetFastApiService(),
            self.GetTokenService(),
            self.GetSessionService(),
            self.GetTokenChecker()
        )
        PostsController(
            self.GetFastApiService(),
            self.GetSessionService()
        )

        TagController(
            self.GetFastApiService(),
            self.GetSessionService()
        )
        ProjectController(
            self.GetFastApiService(),
            self.GetSessionService()
        )

    def GetTokenChecker(self) : 
        if not self._tokenChecker : 
            self._tokenChecker = TokenChecker(
                self.GetConfigurationService()
            )
        return self._tokenChecker

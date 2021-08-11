from Startup.FastApiService import FastApiService
from Application.Service.ConfigurationService import ConfigurationService
import uvicorn
from fastapi.applications import FastAPI






class UvicornService() : 

    _fastApiService:FastApiService
    _configurationService:ConfigurationService

    def __init__(self, fastApiService:FastApiService, configurationService:ConfigurationService) -> None:
        self._fastApiService = fastApiService
        self._configurationService = configurationService

    def Run(self) : 
        uvicorn.run(self._fastApiService._fastApi, host=self._configurationService.GetUvicornHost(), port=self._configurationService.GetUvicornPort())


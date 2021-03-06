import os
from Application.Middlewares.AlchemyItemNotFound import AlchemyItemNotFound
from fastapi.applications import FastAPI
from Application.Service.ConfigurationService import ConfigurationService
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

class FastApiService() : 

    _configurationService:ConfigurationService
    _fastApi:FastAPI

    def __init__(self, configurationService:ConfigurationService) :
        self._configurationService = configurationService
        self._fastApi = FastAPI(title = self._configurationService.GetFastApiTitle())
        self.ActivateMiddlewares()
        self.ActivateCORS()
        self.ActivateStaticFiles()

    def ActivateMiddlewares(self) : 
        self._fastApi.middleware('http')(AlchemyItemNotFound.OnException)

    def ActivateCORS(self) : 
        self._fastApi.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def ActivateStaticFiles(self) : 
        self._fastApi.mount("/files/images", StaticFiles(directory=os.path.join(os.getcwd(),'Static', 'Images'), html = True))
        


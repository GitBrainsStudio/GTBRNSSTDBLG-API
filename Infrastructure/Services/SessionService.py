from Application.Service.ConfigurationService import ConfigurationService
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker




class SessionService() : 

    _configurationService:ConfigurationService
    _sessionMaker:sessionmaker
    _engine:Engine
    __dbContext:Session

    def __init__(self, configurationService:ConfigurationService) :
        self._configurationService = configurationService
        self.__dbContext = None
        self._sessionMaker = sessionmaker
        self._engine = create_engine(
            self._configurationService.GetSQLiteConnectionString())

    def GetDBContext(self) -> Session :
        if not self.__dbContext :
            self.__dbContext = self._sessionMaker(self._engine)()
        return self.__dbContext
        
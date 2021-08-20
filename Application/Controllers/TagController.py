from Application.Service.TokenService import TokenService
from Infrastructure.Services.SessionService import SessionService
from Startup.FastApiService import FastApiService
import uuid
from fastapi.responses import JSONResponse
from Domain.Entities.Tag import Tag
from Application.Dtos.Tags.TagCreate import TagCreate
from Application.Dtos.Tags.TagDelete import TagDelete
from Application.Dtos.Tags.TagUpdate import TagUpdate


class TagController() : 

    _sessionService:SessionService
    _fastApiService:FastApiService
    _tokenService:TokenService

    def __init__(
        self,
        fastApiService:FastApiService,
        sessionService:SessionService,
        tokenService:TokenService) -> None:
        self._tokenService = tokenService
        self._fastApiService = fastApiService
        self._fastApiService._fastApi.add_api_route(path="/tags", endpoint=self.GetAll, methods=["GET"])
        # self._fastApiService._fastApi.add_api_route(path="/tags/{tagId}", endpoint=self.GetById, methods=["GET"])
        # self._fastApiService._fastApi.add_api_route(path="/tags/", endpoint=self.Create, methods=["POST"])
        # self._fastApiService._fastApi.add_api_route(path="/tags/", endpoint=self.Update, methods=["PUT"])
        # self._fastApiService._fastApi.add_api_route(path="/tags/{tagId}", endpoint=self.Delete, methods=["DELETE"])
        self._sessionService = sessionService

    def GetById(self, tagId:str) : 
        return self._sessionService.GetDBContext().query(Tag).filter(Tag.Id == tagId).one()

    def GetAll(self) : 
        return self._sessionService.GetDBContext().query(Tag).all()

    def Update(self, tagUpdate:TagUpdate) : 
        tag:Tag = self._sessionService.GetDBContext().query(Tag).filter(Tag.Id == tagUpdate.Id).one()
        tag.Update(tagUpdate.Title)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Тег успешно обновлен", "id" : tag.Id})

    def Create(self, tagCreate:TagCreate) : 

        tag:Tag = Tag(
            str(uuid.uuid4()),
            tagCreate.Title
        )

        self._sessionService.GetDBContext().add(tag)
        try : 
            self._sessionService.GetDBContext().commit()
        
        except: 
            self._sessionService.GetDBContext().rollback()
        
        return JSONResponse(status_code=200, content={"message": "Тег успешно добавлен", "id" : tag.Id})

    def Delete(self, tagDelete:TagDelete) :
        tag:Tag = self._sessionService.GetDBContext().query(Tag).filter(Tag.Id == tagDelete.Id).one()
        self._sessionService.GetDBContext().delete(tag)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Тег успешно удален"})
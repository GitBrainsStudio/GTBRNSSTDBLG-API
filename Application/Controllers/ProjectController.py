from Infrastructure.Services.SessionService import SessionService
from Startup.FastApiService import FastApiService
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from Domain.Entities.Project import Project
from Application.Dtos.Projects.ProjectCreate import ProjectCreate
from Application.Dtos.Projects.ProjectDelete import ProjectDelete
from Application.Dtos.Projects.ProjectUpdate import ProjectUpdate


class ProjectController() : 

    _sessionService:SessionService
    _fastApiService:FastApiService

    def __init__(
        self,
        fastApiService:FastApiService,
        sessionService:SessionService) -> None:
        self._fastApiService = fastApiService
        self._fastApiService._fastApi.add_api_route(path="/projects", endpoint=self.GetAll, methods=["GET"])
        self._fastApiService._fastApi.add_api_route(path="/projects/{projectId}", endpoint=self.GetById, methods=["GET"])
        self._fastApiService._fastApi.add_api_route(path="/projects/", endpoint=self.Create, methods=["POST"])
        self._fastApiService._fastApi.add_api_route(path="/projects/", endpoint=self.Update, methods=["PUT"])
        self._fastApiService._fastApi.add_api_route(path="/projects/{projectId}", endpoint=self.Delete, methods=["DELETE"])
        self._sessionService = sessionService

    def GetById(self, projectId:str) : 
        return self._sessionService.GetDBContext().query(Project).filter(Project.Id == projectId).one()

    def GetAll(self) : 
        return self._sessionService.GetDBContext().query(Project).all()

    def Update(self, projectUpdate:ProjectUpdate) : 
        project:Project = self._sessionService.GetDBContext().query(Project).filter(Project.Id == projectUpdate.Id).one()
        project.Update(projectUpdate.Title, projectUpdate.Description)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Проект успешно обновлен", "id" : project.Id})

    def Create(self, projectCreate:ProjectCreate) : 

        project:Project = Project(
            str(uuid.uuid4()),
            projectCreate.Title,
            projectCreate.Description
        )

        self._sessionService.GetDBContext().add(project)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Проект успешно добавлен", "id" : project.Id})

    def Delete(self, projectDelete:ProjectDelete) :
        project:Project = self._sessionService.GetDBContext().query(Project).filter(Project.Id == projectDelete.Id).one()
        self._sessionService.GetDBContext().delete(project)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Проект успешно удален"})
from Domain.Entities.Image import Image
from Application.Dtos.Images.ImageUpload import ImageUpload
from Application.Service.TokenService import TokenService
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from Domain.Entities.Tag import Tag
from Infrastructure.Services.SessionService import SessionService
from Application.Dtos.Posts.PostUpdate import PostUpdate
from Startup.FastApiService import FastApiService
from Application.Dtos.Posts.PostCreate import PostCreate
from Application.Dtos.Posts.PostDelete import PostDelete
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from Domain.Entities.Post import Post
from sqlalchemy import func
from fastapi import Depends
import base64



class PostsController() : 

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
        self._fastApiService._fastApi.add_api_route(path="/posts/", endpoint=self.GetAll, methods=["GET"])
        self._fastApiService._fastApi.add_api_route(path="/posts/{postId}", endpoint=self.GetById, methods=["GET"])
        self._fastApiService._fastApi.add_api_route(path="/posts/", endpoint=self.Create, methods=["POST"], dependencies=[Depends(self._tokenService.Check)])
        self._fastApiService._fastApi.add_api_route(path="/posts/", endpoint=self.Update, methods=["PUT"], dependencies=[Depends(self._tokenService.Check)])
        self._fastApiService._fastApi.add_api_route(path="/posts/", endpoint=self.Delete, methods=["DELETE"], dependencies=[Depends(self._tokenService.Check)])
        self._sessionService = sessionService

    def GetById(self, postId:str) : 
        return self._sessionService.GetDBContext().query(Post).filter(Post.Id == postId).one()

    def GetAll(self) : 
        return self._sessionService.GetDBContext().query(Post).all()

    def Update(self, postUpdate:PostUpdate) : 
        post:Post = self._sessionService.GetDBContext().query(Post).filter(Post.Id == postUpdate.Id).one()

        postTags:List[Tag] = []
        for tagTitle in postUpdate.TagsTitles : 

            try :
                postTags.append(self._sessionService.GetDBContext().query(Tag).filter(func.lower(Tag.Title) == func.lower(tagTitle)).one())
                
            except NoResultFound : 

                tag:Tag = Tag(
                    str(uuid.uuid4()),
                        tagTitle
                )

                self._sessionService.GetDBContext().add(tag)
                postTags.append(tag)


        post.Update(postUpdate.Title, postUpdate.Content, postTags)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Пост успешно обновлен", "id" : post.Id})

    def Create(self, postCreate:PostCreate) : 

        postTags:List[Tag] = []
        for tagTitle in postCreate.TagsTitles : 

            try :
                postTags.append(self._sessionService.GetDBContext().query(Tag).filter(func.lower(Tag.Title) == func.lower(tagTitle)).one())
                
            except NoResultFound : 

                tag:Tag = Tag(
                    str(uuid.uuid4()),
                        tagTitle
                )

                self._sessionService.GetDBContext().add(tag)
                postTags.append(tag)
        
        postImages:List[Image] = []
        for imageTitle in postCreate.ImagesTitles : 

            image:Image = Image(
                str(uuid.uuid4()),
                imageTitle,
                datetime.now().strftime("%m/%d/%Y"),
                '17f1c408-28bd-4bde-90b3-a33279a8ba9d'
            )

            self._sessionService.GetDBContext().add(image)
            postImages.append(image)

    
        post:Post = Post(
            str(uuid.uuid4()),
            postCreate.Title,
            postCreate.Content,
            datetime.now().strftime("%m/%d/%Y"),
            '17f1c408-28bd-4bde-90b3-a33279a8ba9d',
            postTags,
            postImages
        )

        self._sessionService.GetDBContext().add(post)

        try :
            self._sessionService.GetDBContext().commit()
        except : 
            self._sessionService.GetDBContext().rollback()
        
        return JSONResponse(status_code=200, content={"message": "Пост успешно добавлен", "id" : post.Id})

    def Delete(self, postDelete:PostDelete) :
        post:Post = self._sessionService.GetDBContext().query(Post).filter(Post.Id == postDelete.Id).one()
        self._sessionService.GetDBContext().delete(post)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Пост успешно удален"})

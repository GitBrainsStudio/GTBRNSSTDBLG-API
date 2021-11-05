from Application.Dtos.Images.ImageDelete import ImageDelete
import os
from Application.Service.ConfigurationService import ConfigurationService
from Application.Service.FileNamingService import FileNamingService
from Application.Dtos.Images.ImageUpload import ImageUpload
from Application.Service.TokenService import TokenService
from Infrastructure.Services.SessionService import SessionService
from Startup.FastApiService import FastApiService
from Domain.Entities.Image import Image
import base64
import uuid
from datetime import datetime
from fastapi.responses import JSONResponse

class ImagesController() : 

    _sessionService:SessionService
    _fastApiService:FastApiService
    _tokenService:TokenService
    _fileNamingService:FileNamingService
    _configurationService:ConfigurationService

    def __init__(
        self,
        fastApiService:FastApiService,
        sessionService:SessionService,
        tokenService:TokenService,
        fileNamingService:FileNamingService,
        configurationService:ConfigurationService) -> None:
        self._tokenService = tokenService
        self._fastApiService = fastApiService
        self._fastApiService._fastApi.add_api_route(path="/images", endpoint=self.Upload, methods=["POST"])
        self._fastApiService._fastApi.add_api_route(path="/images", endpoint=self.Delete, methods=["DELETE"])
        self._sessionService = sessionService
        self._fileNamingService = fileNamingService
        self._configurationService = configurationService

    def Upload(self, imageUpload:ImageUpload) :

        imageBytes = imageUpload.Bytes.encode(encoding='UTF-8')
        image_64_decode = base64.decodebytes(imageBytes)

        imageName = self._fileNamingService.GetRandomFileName(20) + ".jpg"
        imageDir = os.path.join(os.getcwd(),'Static', 'Images', imageName) 

        with open(imageDir, 'wb') as fh:
            fh.write(image_64_decode)

        image:Image = Image(
            str(uuid.uuid4()),
            imageName,
            datetime.now().strftime("%m/%d/%Y"),
             '17f1c408-28bd-4bde-90b3-a33279a8ba9d'
        )

        self._sessionService.GetDBContext().add(image)
        self._sessionService.GetDBContext().commit()
        

        return self._sessionService.GetDBContext().query(Image).filter(Image.Id == image.Id).one()


    def Delete(self, imageDelete:ImageDelete) : 

        image:Image = self._sessionService.GetDBContext().query(Image).filter(Image.Id == imageDelete.Id).one()
        self._sessionService.GetDBContext().delete(image)
        self._sessionService.GetDBContext().commit()
        return JSONResponse(status_code=200, content={"message": "Изображение успешно удалено"})

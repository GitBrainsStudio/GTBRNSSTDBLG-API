import os
from Application.Service.ConfigurationService import ConfigurationService
from Application.Service.FileNamingService import FileNamingService
from Application.Dtos.Images.ImageUpload import ImageUpload
from Application.Service.TokenService import TokenService
from Infrastructure.Services.SessionService import SessionService
from Startup.FastApiService import FastApiService
import base64



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

        return imageName
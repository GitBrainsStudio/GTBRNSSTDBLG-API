from Startup.DependenciesService import DependenciesService




_dependenciesService:DependenciesService
_dependenciesService = DependenciesService()
_dependenciesService.RegisterControllers()
_dependenciesService.GetUvicornService().Run()

def GetFastApi() : 
    return _dependenciesService.GetFastApiService()._fastApi
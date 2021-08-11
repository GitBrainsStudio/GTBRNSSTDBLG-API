from Startup.DependenciesService import DependenciesService








class Main() : 

    _dependenciesService:DependenciesService

    def __init__(self) -> None:
        self._dependenciesService = DependenciesService()
        self._dependenciesService.RegisterControllers()
        self._dependenciesService.GetUvicornService().Run()
      
Main()
import json








class ConfigurationService() : 

    _configurationData:any

    def __init__(self) :
        self.ReadConfigurationFile()
    
    def ReadConfigurationFile(self) : 
        with open('C:\\Users\\User98\\Desktop\\GitBrainsBlog\\Api\\Application\\Configurations\\Web.config.json', 'r') as configurationFile:
            self._configurationData = json.load(configurationFile)

    def GetSQLiteConnectionString(self) :
        return self._configurationData["sqliteConnectionString"]

    def GetFastApiTitle(self) : 
        return self._configurationData["fastApiTitle"]

    def GetUvicornHost(self) : 
        return self._configurationData["host"]

    def GetUvicornPort(self) : 
        return self._configurationData["port"]

    def GetTokenAlgorithm(self) : 
        return self._configurationData["tokenAlgorithm"]

    def GetTokenSecretKey(self) : 
        return self._configurationData["tokenSecretKey"]

        
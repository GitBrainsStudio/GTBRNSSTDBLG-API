import random
import string

class FileNamingService() : 

    def GetRandomFileName(self, fileNameLength:int) : 
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(fileNameLength))
        
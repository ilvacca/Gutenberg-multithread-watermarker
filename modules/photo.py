import time, os
from PIL import Image


class Photo:
    
    def __init__(self, path, verbose = False):
        self._objectName = "PHOTO"
        self._objectLevel = 3
        self._verbose = verbose
        self.path = path
        self.image = Image.open(path)
        self.name = os.path.basename(self.path)
        
    # LOGGER ################################################################################

    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)
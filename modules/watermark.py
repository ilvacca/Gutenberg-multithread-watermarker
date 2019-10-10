import time
from PIL import Image
from tkinter import Tk, filedialog

class Watermark:
    
    def __init__(self, verbose = False):
        self._objectName = "WATERMARK"
        self._objectLevel = 2
        self._verbose = verbose

    # SELECT/LOAD ############################################################################

    def setPath(self, watermarkPath):
        if watermarkPath != "":
            self.isSelected = True
            self.path = watermarkPath
        else:
            self.isSelected = False
            self.path = ""
        
    def load(self):
        self.sourceImage = Image.open(self.path)
        self.readyImage = self.sourceImage
    
    def reset(self):
        self.path = None
        self.sourceImage = None
        self.readyImage = None
        
    # READY IMAGE ###########################################################################
    
    def setReadyImage(self, readyImage):
        self.readyImage = readyImage

    def getReadyImage(self):
        return(self.readyImage)
        
    def resetReadyImage(self):
        self.readyImage = self.sourceImage
    
    # LOGGER ################################################################################

    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)
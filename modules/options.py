import time

class Options:
    
    def __init__(self, verbose = False):
        self._objectName = "OPTIONS"
        self._objectLevel = 2
        self._verbose = verbose
        self.setDefault()

    # SETTER ################################################################################
    
    def setDefault(self):
        self.watermarkDestinationBrightness = 1
        self.watermarkDestinationSizePercentage = 0.10
        self.watermarkDestinationCoordinates = (0,0)
        self.watermarkDestinationOffsetPercentage = 0
        
    def setWatermarkDestinationBrightness(self, destBrightness):
        self.watermarkDestinationBrightness = destBrightness
        self._logger("Watermark destination brightness is now '%s'" % self.watermarkDestinationBrightness)
        
    def setWatermarkDestinationSizePercentage(self, destSizePercentage):
        self.watermarkDestinationSizePercentage = destSizePercentage
        self._logger("Watermark destination size percentage is now '%s'" % self.watermarkDestinationSizePercentage)
        
    def setWatermarkDestinationCoordinates(self, destCoordinates):
        self.watermarkDestinationCoordinates = destCoordinates
        self._logger("Watermark destination coordinates are now '%s'" % str(self.watermarkDestinationCoordinates))
    
    def setWatermarkDestinationOffsetPercentage(self, destOffsetPercentage):
        self.watermarkDestinationOffsetPercentage = destOffsetPercentage
        self._logger("Watermark destination offset percentage is now '%s'" % str(self.watermarkDestinationOffsetPercentage))

    def setOutputFolder(self, outputFolderPath):
        self.outputFolder = outputFolderPath
        self._logger("Output folder is now '%s'" % str(self.outputFolder))

    def setOutputSuffix(self, outputSuffix):
        self.outputSuffix = outputSuffix
        self._logger("Output suffix is now '%s'" % str(self.outputSuffix))

    def setOutputPrefix(self, outputPrefix):
        self.outputPrefix = outputPrefix
        self._logger("Output prefix is now '%s'" % str(self.outputPrefix))
    
    # SHOW ##################################################################################
    
    def show(self):
        result = "".join(["%s: %s\n"%(key, self.__dict__[key]) for key in self.__dict__ if key[0] != "_"])
        print(result)
    
    # LOGGER ################################################################################
    
    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)
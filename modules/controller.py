from modules.watermark import Watermark
from modules.engine import Engine
from modules.options import Options
from modules.photo import Photo
from modules.bucket import Bucket
from modules.iomanager import IOManager
import time

class Controller:
    
    def __init__(self, verbose = False):
        self._objectName = "CONTROLLER"
        self._objectLevel = 1
        self._verbose = verbose
        self.bucket = Bucket()
        self.watermark = Watermark()
        self.options = Options()
        self.engine = Engine()
        self.iomanager = IOManager()

    # LOADING ################################################################################

    def bucketIsReady(self):
        return(self.bucket.isFilled)

    def watermarkIsReady(self):
        return(self.watermark.isSelected)

    def fillBucket(self):
        self.bucket.fill()
        if self.bucket.isFilled:
            return(True)
        else:
            return(False)

    def loadWatermark(self):  
        wmp = self.iomanager.askWatermarkPath()
        self.watermark.setPath(wmp)
        if self.watermark.isSelected:
            self.watermark.load()
            return(True)
        else:
            return(False)

    def resetWatermark(self):
        self.watermark.reset()

    # OPTIONS SETTING ########################################################################

    def setWatermarkDestinationBrightness(self, brightness):
        self.options.setWatermarkDestinationBrightness(brightness)

    def setWatermarkDestinationOffsetPercentage(self, offsetPerc):
        self.options.setWatermarkDestinationOffsetPercentage(offsetPerc)

    def setWatermarkDestinationSizePercentage(self, sizePerc):
        self.options.setWatermarkDestinationSizePercentage(sizePerc)

    def setOutputPrefix(self, outputPrefix):
        self.options.setOutputPrefix(outputPrefix)

    def setOutputSuffix(self, outputSuffix):
        self.options.setOutputSuffix(outputSuffix)

    def setOutputFolder(self):
        outputFolder = self.iomanager.askOutputFolder()
        self.options.setOutputFolder(outputFolder)
    
    def resetOutputFolder(self):
        cwd = self.iomanager.resetOutputFolder()
        self.options.setOutputFolder(cwd)

    # GET THE JOB DONE ######################################################################

    def process(self):
        watermark = self.watermark
        bucket = self.bucket
        options = self.options
        self.engine.parallelMerge(bucket, watermark, options)

    def serialProcess(self):
        watermark = self.watermark
        bucket = self.bucket
        options = self.options
        self.engine.serialMerge(bucket, watermark, options)

    # LOGGER ################################################################################

    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)
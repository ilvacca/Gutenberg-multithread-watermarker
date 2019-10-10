import time
from modules.controller import Controller


class Interface:

    def __init__(self, verbose = False):
        self._objectName = "INTERFACE"
        self._objectLevel = 0
        self._verbose = verbose
        self.controller = Controller()

    # WELCOME! ###############################################################################

    def welcomeMessage(self):
        print("## WELCOME TO GUTENBERG")
        print("## A batch watermark applicator tool")
        print("## ----------------------------------------------------------------")
        print("## Made with love by Alessio Vaccaro")
        print("## www.alessiovaccaro.com")
        print("## ----------------------------------------------------------------")
        print("## Gutenberg is part of the Blue Journey Astrophotography project\n")

    def endingMessage(self):
        input("\n## Please press ENTER to exit...")
        print("## Bye!")
        time.sleep(1)
    
    # QUESTIONS ##############################################################################

    def askForSomething(self, message):
        log = self._loggerReturn(message)
        userInput = input(log)
        return(userInput)

    def askForWatermarkBrightness(self):
        watermarkBrightness = int(self.askForSomething("Please insert watermark brightness [0-100%]: ")) * 0.01
        self.controller.setWatermarkDestinationBrightness(watermarkBrightness)

    def askForWatermarkOffsetPercentage(self):
        watermarkOffsetPercentage = int(self.askForSomething("Please insert watermark offset [0-100%]: ")) * 0.01
        self.controller.setWatermarkDestinationOffsetPercentage(watermarkOffsetPercentage)

    def askForWatermarkSizePercentage(self):
        watermarkSizePercentage = int(self.askForSomething("Please insert watermark size [0-100%]: ")) * 0.01
        self.controller.setWatermarkDestinationSizePercentage(watermarkSizePercentage)

    def askForOutputFolder(self):
        self._logger("Selecting output folder...")
        self.controller.setOutputFolder()
        self._logger("Output folder selected")

    def askForOutputPrefix(self):
        outputPrefix = self.askForSomething("Please output prefix [ex. 'prefix' for 'prefix-myimage.jpg']: ")
        self.controller.setOutputPrefix(outputPrefix)

    def askForOutputSuffix(self):
        outputSuffix = self.askForSomething("Please output suffix [ex. 'suffix' for 'myimage-suffix.jpg']: ")
        self.controller.setOutputSuffix(outputSuffix)

    def askForImages(self):
        selected = False
        tries = 1
        self._logger("Please select images...")
        while (not selected) and (tries < 3):
            if self.controller.fillBucket():
                self._logger("Images selected...") 
                selected = True
            else:
                self._logger("Please select images...")
                tries += 1

    def askForWatermark(self):
        selected = False
        tries = 1
        self._logger("Please select watermark...")
        while (not selected) and (tries < 3):
            if self.controller.loadWatermark():
                self._logger("Watermark selected")
                selected = True
            else:
                self._logger("Please select watermark...")
                tries += 1

    def startTheProcess(self):
        self._logger("Starting...")
        self.controller.process()
        self._logger("Done!")

    # LOOP ##################################################################################

    def loop(self):
        # WELCOME
        self.welcomeMessage()
        # Prepare Bucket and Loading Watermark
        self.askForImages()
        if self.controller.bucketIsReady():
            self.askForWatermark()
            if self.controller.watermarkIsReady():
                # Option setting
                self.askForWatermarkBrightness()
                self.askForWatermarkOffsetPercentage()
                self.askForWatermarkSizePercentage()
                self.askForOutputPrefix()
                self.askForOutputSuffix()
                self.askForOutputFolder()
                # START
                self.startTheProcess()
        # END
        self.endingMessage()

    # LOGGER ################################################################################

    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)

    def _loggerReturn(self, message):
        now = time.strftime("%H:%M:%S", time.localtime())
        message = "%s [%s]: %s" % (now, self._objectName, message)
        return(message)

from tkinter import Tk, filedialog
import os, time

class IOManager:

    def __init__(self, verbose = False):
        self._objectName = "IOMANAGER"
        self._objectLevel = 2
        self._verbose = verbose

    # WATERMARK FOLDER ######################################################################

    def askWatermarkPath(self):
        Tk().withdraw()
        wmPath = filedialog.askopenfilename(title="Select the watermark",filetype=(("PNG files","*.png"),))
        return(wmPath)

    # OUTPUT FOLDER #########################################################################

    def resetOutputFolder(self):
        self._logger("Resetting output folder...")
        outputFolder = os.getcwd()
        self._logger("Output folder reset")
        return(outputFolder)

    def askOutputFolder(self):
        self._logger("Selecting output folder...")
        Tk().withdraw()
        outputFolder = filedialog.askdirectory()
        self._logger("Output folder selected")
        return(outputFolder)

    # LOGGER ################################################################################

    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)
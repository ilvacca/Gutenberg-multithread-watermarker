from PIL import Image, ImageEnhance
import time, os
from multiprocessing import Pool
from itertools import product
from modules.photo import Photo
import numpy as np


class Engine:
    
    def __init__(self, verbose = False):
        self._objectName = "ENGINE"
        self._objectLevel = 2
        self._verbose = 0
        
    # CALCULATIONS ##########################################################################
    
    def _calculateWatermarkDestinationWidth(self, photo, options):
        destSizePercentage = options.watermarkDestinationSizePercentage
        destinationWidth = int(round(destSizePercentage * photo.image.width,0))
        return(destinationWidth)
    
    def _calculateWatermarkDestinationOffset(self, photo, options):
        destinationOffset = photo.image.size[0] * options.watermarkDestinationOffsetPercentage
        destinationOffset = int(round(destinationOffset,0))
        return(destinationOffset)
    
    def _calculateWatermarkCoordinates(self, photo, watermarkImage, options):
        offset = self._calculateWatermarkDestinationOffset(photo, options)
        rawX, rawY = photo.image.size
        fgW, fgH = watermarkImage.size[0], watermarkImage.size[1]
        LUx, LUy = rawX-offset-fgW, rawY-offset-fgH
        BDx, BDy = rawX-offset, rawY-offset
        destinationCoordinates = (LUx, LUy, BDx, BDy)
        return(destinationCoordinates)
        
    # WATERMARK PROCESSING ###################################################################
    
    def processWatermark(self, photo, watermark, options):
        resultWatermarkTuple = self._processWatermarkOpacity(watermark, options)
        resultWatermarkTuple = self._processWatermarkResizing(photo, resultWatermarkTuple, options)
        return(resultWatermarkTuple)
    
    def _processWatermarkOpacity(self, watermarkTuple, options):
        resultWatermarkImage = watermarkTuple.sourceImage
        alphaImage = watermarkTuple.sourceImage.split()[-1]
        opacity = options.watermarkDestinationBrightness
        #enhancer = ImageEnhance.Brightness(resultAlphaImage)
        #resultAlphaImage = enhancer.enhance(brightness)
        resultAlphaImage = Image.fromarray((np.array(alphaImage)*opacity).astype("uint8"))
        return(resultWatermarkImage, resultAlphaImage)
    
    def _processWatermarkResizing(self, photo, watermarkTuple, options):
        watermarkImage = watermarkTuple[0]
        alphaImage = watermarkTuple[1]
        w, h = watermarkImage.size
        watermarkDestinationWidth = self._calculateWatermarkDestinationWidth(photo, options)
        resultWatermarkImage = watermarkImage.resize((watermarkDestinationWidth, int(h*(watermarkDestinationWidth/w))), Image.BILINEAR)
        resultAlphaImage = alphaImage.resize((watermarkDestinationWidth, int(h*(watermarkDestinationWidth/w))), Image.BILINEAR)
        return(resultWatermarkImage, resultAlphaImage)
        
    # MERGER ################################################################################
    
    def _buildOutputImageCompletePath(self, image, options):
        name, extension = os.path.splitext(image.basename)
        folder = options.outputFolder
        if options.outputPrefix != "":
            name = "%s-%s" % (options.outputPrefix, name)
        if options.outputSuffix != "":
            name = "%s-%s" % (name, options.outputSuffix)
        completePath = "%s/%s%s"% (folder,name,extension)
        return(completePath)

    def _merge(self, photoPath, watermark, options):
        self._logger("Merging image with watermark...")
        photo = Photo(photoPath)
        watermarkImage, alphaImage  = self.processWatermark(photo, watermark, options)
        destinationCoords = self._calculateWatermarkCoordinates(photo, watermarkImage, options)
        resultImage = photo.image
        resultImage.paste(watermarkImage, destinationCoords, alphaImage)
        resultImage.basename = photo.name
        del(photo)
        self._logger("Merged image with watermark")
        return(resultImage)

    def _saveImage(self, image, options):
        self._logger("Saving image...")
        completePath = self._buildOutputImageCompletePath(image, options)
        exif = image.info["exif"] if image.format != 'PNG' else ""
        image.save(completePath, quality=95, exif=exif)
        self._logger("Image saved")

    def _mergeAndSave(self, photoPath, watermark, options):
        self._logger("Merging watermark with '%s'..." % photoPath)
        resultImage = self._merge(photoPath, watermark, options)
        self._saveImage(resultImage, options)
        self._logger("Merged and saved")
    
    def parallelMerge(self, bucket, watermark, options):
        cores = os.cpu_count()
        p = Pool(cores)
        bucket = bucket.bucket
        results = p.starmap(self._mergeAndSave, product(bucket,[watermark],[options]))

    def serialMerge(self, bucket, watermark, options):
        [self._mergeAndSave(photoPath, watermark, options) for photoPath in bucket.bucket]
        
    # LOGGER ################################################################################

    def _logger(self, message):
        if self._verbose == True:
            now = time.strftime("%H:%M:%S", time.localtime())
            message = "%s [%s]: %s" % (now, self._objectName, message)
            print(message)
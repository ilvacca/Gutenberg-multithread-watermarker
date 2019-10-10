import time
from PIL import Image
from tkinter import Tk, filedialog


class Bucket:

	def __init__(self, verbose = False):
		self._objectName = "BUCKET"
		self._objectLevel = 2
		self._verbose = verbose
		self.empty()
		self.isFilled = False

	# FILL / EMPTY ###########################################################################

	def fill(self):
		Tk().withdraw()
		self.bucket = filedialog.askopenfilenames(title="Select images you want to apply watermark to",filetypes=(
			("JPG files","*.jpg *.jpeg"),("PNG files","*.png"),("TIFF files","*.tiff *.tif"),("ALL files","*.*")
		))
		self.bucketSize = len(self.bucket)
		if self.bucketSize != 0:
			self.isFilled = True
		else:
			self.isFilled = False

	def empty(self):
		self.bucket = []
		self.bucketSize = 0
		self.isFilled = False

	# LOGGER #################################################################################

	def _logger(self, message):
		if self._verbose == True:
			now = time.strftime("%H:%M:%S", time.localtime())
			message = "%s [%s]: %s" % (now, self._objectName, message)
			print(message)
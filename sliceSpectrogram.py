# Import Pillow:
from PIL import Image
import os.path

from config import spectrogramsPath, slicesPath

#Slices all spectrograms
def createSlicesFromSpectrograms(rootPath, desiredSize):
	for filename in os.listdir(rootPath + spectrogramsPath):
		if filename.endswith(".png"):
			sliceSpectrogram(rootPath, filename,desiredSize)

#Creates slices from spectrogram
#TODO Improvement - Make sure we don't miss the end of the song
def sliceSpectrogram(rootPath, filename, desiredSize):
	genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

	# Load the full spectrogram
	img = Image.open(rootPath + spectrogramsPath + filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize

	#Create path if not existing
	slicePath = rootPath + slicesPath+"{}/".format(genre);
	if not os.path.exists(os.path.dirname(rootPath + slicePath)):
		try:
			os.makedirs(os.path.dirname(rootPath + slicePath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#For each sample
	for i in range(nbSamples):
		print "Creating slice: ", (i+1), "/", nbSamples, "for", filename
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save(rootPath + slicesPath+"{}/{}_{}.png".format(genre,filename[:-4],i))

#TODO Improvement - Make sure we don't miss the end of the song
def sliceSpectrogramToIdentify(rootPath, filename, desiredSize):

	# Load the full spectrogram
	img = Image.open(rootPath + spectrogramsPath + filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize

	#Create path if not existing
	slicePath = slicesPath + filename ;
	slicePath = slicePath[:-4] + '/';
	if not os.path.exists(os.path.dirname(rootPath + slicePath)):
		try:
			os.makedirs(os.path.dirname(rootPath + slicePath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#For each sample
	for i in range(nbSamples):
		print "Creating slice: ", (i+1), "/", nbSamples, "for", filename
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save(rootPath + slicePath  + "{}_{}.png".format(filename[:-4],i))

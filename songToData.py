# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image
import eyed3

from sliceSpectrogram import createSlicesFromSpectrograms
from audioFilesTools import isMono, getGenre
from config import rawDataPath
from config import spectrogramsPath
from config import pixelPerSecond

_rootPath = ""
#Tweakable parameters
desiredSize = 128

#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 

#Remove logs
eyed3.log.setLevel("ERROR")

#Create spectrogram from mp3 files
def createSpectrogram(rootPath,filename,newFilename):
	#Create temporary mono track if needed
	if isMono(_rootPath + rawDataPath+filename):
		command = "cp '{}' '/tmp/{}.mp3'".format(rootPath + rawDataPath + filename,newFilename)
	else:
		command = "sox '{}' '/tmp/{}.mp3' remix 1,2".format(_rootPath + rawDataPath + filename,newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print errors

	#Create spectrogram
	filename.replace(".mp3","")
	command = "sox '/tmp/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(newFilename,pixelPerSecond, rootPath + spectrogramsPath + newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print errors

	#Remove tmp mono track
	os.remove("/tmp/{}.mp3".format(newFilename))

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio(rootPath):
	genresID = dict()
	files = os.listdir(rootPath + rawDataPath)
	files = [file for file in files if file.endswith(".mp3")]
	nbFiles = len(files)

	#Create path if not existing
	if not os.path.exists(os.path.dirname(rootPath + spectrogramsPath)):
		try:
			os.makedirs(os.path.dirname(rootPath + spectrogramsPath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#Rename files according to genre
	for index,filename in enumerate(files):
		print "Creating spectrogram for file {}/{}...".format(index+1,nbFiles)
		fileGenre = getGenre(rootPath + rawDataPath + filename)
		genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
		fileID = genresID[fileGenre]
		if fileGenre is not None:
			newFilename = fileGenre+"_"+fileID
			createSpectrogram(rootPath, filename,newFilename)
		else:
			print("couldn't identify genre for " + filename)

#Whole pipeline .mp3 -> .png slices
def createSlicesFromAudio(rootPath):
	_rootPath = rootPath
	print "Creating spectrograms..."
	createSpectrogramsFromAudio(rootPath)
	print "Spectrograms created!"

	print "Creating slices..."
	createSlicesFromSpectrograms(rootPath,desiredSize)
	print "Slices created!"
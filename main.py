# -*- coding: utf-8 -*-
import random
import string
import os
import sys
import numpy as np

from model import createModel
from datasetTools import getDataset
from config import slicesPath
from config import batchSize
from config import filesPerGenre
from config import nbEpoch
from config import validationRatio, testRatio
from config import sliceSize
from config import trainPath
from config import identifyPath

from songToData import createSlicesFromAudio

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains or tests the CNN", nargs='+', choices=["train","test","slice","identify"])
args = parser.parse_args()

print("--------------------------")
print("| ** Config ** ")
print("| Validation ratio: {}".format(validationRatio))
print("| Test ratio: {}".format(testRatio))
print("| Slices per genre: {}".format(filesPerGenre))
print("| Slice size: {}".format(sliceSize))
print("--------------------------")

if "slice" in args.mode:
	createSlicesFromAudio(trainPath)
	sys.exit()

#List genres
genres = os.listdir(trainPath + slicesPath)
genres = [filename for filename in genres if os.path.isdir(trainPath + slicesPath + filename)]
nbClasses = len(genres)

#Create model 
model = createModel(nbClasses, sliceSize)

if "train" in args.mode:

	#Create or load new dataset
	train_X, train_y, validation_X, validation_y = getDataset(trainPath, filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="train")

	#Define run id for graphs
	run_id = "MusicGenres - "+str(batchSize)+" "+''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(10))

	#Train the model
	print("[+] Training the model...")
	model.fit(train_X, train_y, n_epoch=nbEpoch, batch_size=batchSize, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
	print("    Model trained! ✅")

	#Save trained model
	print("[+] Saving the weights...")
	model.save('musicDNN.tflearn')
	print("[+] Weights saved! ✅💾")

if "test" in args.mode:

	#Create or load new dataset
	test_X, test_y = getDataset(trainPath, filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")

	#Load weights
	print("[+] Loading weights...")
	model.load('musicDNN.tflearn')
	print("    Weights loaded! ✅")

	testAccuracy = model.evaluate(test_X, test_y)[0]
	print("[+] Test accuracy: {} ".format(testAccuracy))


# need to check, i write on blind
if "identify" in args.mode:
	print("[+] Start to identify...")
	createSlicesFromAudio(identifyPath)
	sys.exit()
	# Create or load new dataset
	identify_X, identify_y = getDataset(identifyPath, filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="identify")


	# Load weights
	print("[+] Loading weights...")
	model.load('musicDNN.tflearn')
	print("    Weights loaded! ✅")

	testAccuracy = model.evaluate(identify_X, identify_y)[0]

	#now we need to debug and understand how the vector identify_x and identify_y is built and like that print the song name, the Prediction genre and the truth
	# and understand how the testAccuracy built to get the Prediction
	for i in range(len(identify_y)):
		print('song {} was classified as {}'.format(fileNames[i], alphabet[results[i]]))

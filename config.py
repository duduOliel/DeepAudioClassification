#Define paths for files
trainPath = "Data/"
identifyPath = "Identify/"

spectrogramsPath = "Spectrograms/"
slicesPath = "Slices/"
datasetPath = "Dataset/"
rawDataPath = "Raw/"
outputPath = "output/"

#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128

#Dataset parameters
filesPerGenre = 1000
validationRatio = 0.3
testRatio = 0.1

#Model parameters
batchSize = 128
learningRate = 0.001
nbEpoch = 20
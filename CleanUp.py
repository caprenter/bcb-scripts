import os
import re

"""
Script to clean up the Audio directory on the Myriad server

The directory gets poluted with rogue files such as .mp3s, word documents, etc

This script moves suspect files to a 'delete' directory


Usage:
	Set up your basepath to the Audio directory
	Create a new 'delete' directory inside that basepath directory
	run CleanUp.py
"""

# Set some variables
basepath = '/home/david/Desktop/python_fun/Audio'
#files_to_keep = ['Audwall', 'MYRD_SYS'] # Note used yet. NB we also want to keep files that start with "PSQ"
# A tuple of file extensions that we want to keep. all of the below are legit
extensions_to_keep = ('.WAV', '.wav', '.lst', '.LST', '.ini', '.INI', '.pk', '.RTF', '.RT')

### First task is to remove any files that should not be in there by extension e.g jpg, m4a, mpg, whatevs ###
### Second task is to filter out bad WAV files by filename ###

## Task 1 ##
#Get all the files we want to check - make sure we skip directories
OurFiles = [] #listdir(dir)
for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
        # skip directories
        continue
    else:
		OurFiles.append(fname)

#Find the bad files we don't want to be there
badFiles =[]

for file in OurFiles:
	if not file.endswith(extensions_to_keep):
		badFiles.append(file)

print(badFiles)

# Move the bad files to the 'delete' directory
for file in badFiles:
	os.rename(basepath + '/' + file, basepath + "/delete/" + file)
	print("Moving " + file)
	
## Task 2 ##
# Second task is to filter out bad WAV files by filename

# Check only the files with these extensions
wav_ex = ('.WAV', '.wav')

# Fetach all the wav files
wavs = [] #listdir(dir)
for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
       # skip directories
        continue
    else:
		wavs.append(fname)

# Weed out the bad wavs
badwavs =[]

for file in wavs:
	if file.endswith(wav_ex): #let WAV and wav through
		if not re.match(r'(^PSQ)', file): #Lets anything that is not PSQxxxx through
			if not len(file) == 12:  #lets anything that is 12 charachters long through MYR12345.WAV for example
				if not re.match(r'(^(MYR|myr)[0-9]{5}(\.WAV$|\.wav$))', file):	# MYR, has 5 digits and ends with .WAV or .wav
					badwavs.append(file)

print(badwavs)

# Move the bad wavs to the 'delete' directory
for file in badwavs:
	os.rename(basepath + '/' + file, basepath + "/delete/" + file)
	print("Moving " + file)
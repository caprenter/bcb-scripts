import os
#from os import listdir
#from os.path import isfile, join, splitext
#import string
import re
#import zipfile
#import subprocess

#Get the files we want to extract

basepath = '/home/david/Desktop/python_fun/Audio'
#dir = "Audio"

#"""

files_to_keep = ['Audwall', 'MYRD_SYS'] #PSQ
extensions_to_keep = ('.WAV', '.wav', '.lst', '.LST', '.ini', '.INI', '.pk', '.RTF', '.RT')

# First task is to remove any files that should not be in there by extension e.g jpg, m4a, mpg whatevs
# Second task is to filter out bad WAV files by filename

OurFiles = [] #listdir(dir)
for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
        # skip directories
        continue
    else:
		OurFiles.append(fname)


badFiles =[]

for file in OurFiles:
	if not file.endswith(extensions_to_keep):
		badFiles.append(file)

print(badFiles)

for file in badFiles:
	os.rename(basepath + '/' + file, basepath + "/delete/" + file)
	print("Moving " + file)
	
#"""

wavsex = ('.WAV', '.wav')

# Second task is to filter out bad WAV files by filename

wavs = [] #listdir(dir)
for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
       # skip directories
        continue
    else:
		wavs.append(fname)

badwavs =[]

for file in wavs:
	if file.endswith(wavsex): #let WAV and wav through
		if not re.match(r'(^PSQ)', file): #Lets anything that is not PSQxxxx through
			if not len(file) == 12:  #lets anything that is 12 charachters long through MYR12345.WAV for example
				if not re.match(r'(^(MYR|myr)[0-9]{5}(\.WAV$|\.wav$))', file):	
					badwavs.append(file)
					#filter(badwavs) MYR[0-9][0-9][0-9][0-9][0-9])

print(badwavs)

for file in badwavs:
	os.rename(basepath + '/' + file, basepath + "/delete/" + file)
	print("Moving " + file)

#import glob
#for file in badwavs:
#	re.match(r'MYR[0-9][0-9][0-9][0-9][0-9]'
#	glob.glob('MYR[0-9][0-9][0-9][0-9][0-9]')



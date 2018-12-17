import zipfile
import subprocess
from os import listdir
from os.path import isfile, join, splitext
import string
import re
"""
Syed and David are trying to loop over a bunch of Myriad Transport files (.zip)
to extract the data from the .LST files, turn the .WAVs into mp3s with
tags from the LST file
"""

"""
Usage
make sure you have lame installed and that it's in your path 

Place this file in a directory.
Create a 'files' directory in the same place
Create an 'extracted' directory in the same place

Put some Myriad 2.6.x transport files in the 'files' directory.

run 
  python archiver.py
  
"""
	
#Get the files we want to extract
OurFiles = listdir("files")

#Extract them
for ourfile in OurFiles:
	print ourfile
	z = zipfile.ZipFile("files/" + ourfile, "r")
	for filename in z.namelist(  ):
			print 'File:', filename,
			bytes = z.read(filename)
			print 'has',len(bytes),'bytes'
			
	z.extractall("extracted")


#Now they are extracted we want to find all the wavs and their corresponding .LST files
extractedFiles = listdir("extracted")
#waveFiles = listdir("extracted")


##Get the data from the .LST files
listFiles =[]

for file in extractedFiles:
	if file.endswith(".LST"):
		listFiles.append(file)

print(listFiles)

splitter = "      | - "

#Loop over the list files to read and process the data we need for the mp3 tags
for file in listFiles:
	notes = open("extracted/" + file, "r")
	notes = notes.read()	
	#Tries to get rid of guff in the list file
	#notes = notes.strip()
	printable = set(string.printable)
	notes = filter(lambda x: x in printable, notes)
	#A user can only enter 3 lines of 50 characters
	notes = (notes[:150]) if len(notes) > 150 else notes
	notes = notes.strip()
	#Tries to split the strings into useable stuff
	notes = re.split(splitter, notes)
	#notes is now a list
	print (notes)
	
	#While we have the .LST file, we generate the name of the corresponding wav file
	wavfile = splitext("extracted/" + file)[0] + ".WAV"
	
	#Create the mp3
	title = notes[0] #use the 'first' line of the .LST file
	artist = "BCB Radio 106.6FM"
	notes.pop(0) #removes the first item from the list which we have already used for the title
	comment = ', '.join(notes) #uses rest of list items text for the comment
	cmd = 'lame --preset standard --tt "{}" --ta "{}" --tc "{}" {} '.format(title, artist, comment, wavfile)
	subprocess.call(cmd, shell=True)


#for filename in OurFiles:
#    print '%20s  %s' % (filename, zipfile.is_zipfile(filename))

#for ourfile in OurFiles:
#	print ourfile
#	z = zipfile.ZipFile("files/" + ourfile, "r")
	
	
	
"""	
# Convert the wavs to mp3	
for file in waveFiles:
    if file.endswith(".WAV"):
		print(file)
		cmd = 'lame --preset standard %s' % 'extracted/' + file
		subprocess.call(cmd, shell=True)
"""

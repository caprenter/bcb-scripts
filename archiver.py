import zipfile
import subprocess
import os
from os import listdir
from os.path import isfile, join, splitext
import string
import re
import time
import datetime
from pathlib import Path
"""
ABOUT
Syed and David are trying to loop over a bunch of Myriad Transport files (.zip)
to extract the data from the .LST files, turn the .WAVs into mp3s with
tags from the LST file

The transport file can contain a number of files
.WAV - the audio
.LST - a text file that contains up to 150 characters of text over (upto) 3 lines
.DAB - data that could be shown on a DAB radio
.RT - data that would show on a radio text device
.RTF - a rich text format file with some additional information about the audio
"""

"""
USAGE
make sure you have lame installed and that it's in your path 

Place this file in a directory.
Create a 'files' directory in the same place
Create an 'extracted' directory in the same place

Put some Myriad 2.6.x transport files in the 'files' directory.

Edit the set up variables (below) for filenames, albums etc

RUN 
  python3 archiver.py
 
RUN WITH LOGGING
  This will write the print statements to the screen and to a file called log.txt
  python3 -u archiver.py | tee log.txt 
  
The mp3s that are created should be in the same directory as this script, tagged up with suitable information.
Filenames are a mix of a self defined prefix, a count, and a timestamp
  
"""

##Set some variables
# mp3 data
#fileprefix = "BradfordRocks" #for filename
#album = "Bradford Rocks"
fileprefix = "OurTopTen" #for filename
album = "Our Top Ten"
artist = "BCB Radio 106.6FM" # for artist tag
destination_directory = "/OurTopTen_done/"
basepath = "/home/david/Documents/BCB/Scripts/bcb-scripts"


def unzipfile (ourfile):
	z = zipfile.ZipFile("files/" + ourfile, "r")
	#print(z.namelist)
	for filename in z.namelist(  ):
		#print(filename)
		bytes = z.read(filename)
		print ('File: "{}" has "{}" bytes'.format(filename, len(bytes)))

	print("Extracting...")
	z.extractall("extracted")
	print("Files have been extracted")

"""
Wav file might be
MYR11111.WAV, MYR11111.wav, myr11111.wav, myr11111.WAV
(I guess it could be e.g. Myr11111.wav as well...ummm)
"""
def find_wav_file (filename_without_extension):
	wavfile = Path("extracted/" + filename_without_extension + ".WAV")
	if wavfile.is_file():
		return wavfile
	else:
		wavfile = Path("extracted/" + filename_without_extension + ".wav")
	if wavfile.is_file():
		return wavfile
	else: 
		new_name = "myr" + filename_without_extension[3:]
		wavfile = Path("extracted/" + new_name + ".wav")
	if wavfile.is_file():
		return wavfile
	else: 
		wavfile = Path("extracted/" + new_name + ".WAV")
	if wavfile.is_file():
		return wavfile
	else:
		raise SystemExit()
		
			
	
def filter_non_printable(Str):
    return ''.join(s for s in Str if s in string.printable)
	
	
def create_mp3 (file, album, artist):

	#Find the .LST file..
	filename_without_extension = splitext(file)[0]
	#...open it and get the data out
	path = "extracted/" + filename_without_extension + ".LST"
	with open(path, encoding="cp1252", errors='ignore') as f:
		notes = f.read()
	#notes = open("extracted/" + filename_without_extension + ".LST", "r")
	#notes = notes.read()
	print(notes)	
	
	#Tries to get rid of guff in the list file
	#notes = notes.strip()
	notes = filter_non_printable(notes)
	#printable = set(string.printable)
	#notes = ''.join(s for s in notes if s in printable)
	#notes = filter(lambda x: x in printable, notes)
	print (notes)
	
	#A user can only enter 3 lines of 50 characters
	notes = (notes[:150]) if len(notes) > 150 else notes
	notes = notes.strip()
	
	#Tries to split the strings into useable stuff
	#splitter = "      | - "
	splitter = "    "
	notes = re.split(splitter, notes)
	#notes is now a list
	print (notes)
	
	#While we have the .LST file, we generate the name of the corresponding wav file
	#NB .LST file may not have the same sort of name as the wav file - we can have lowercase myr and wav
	wavfile = find_wav_file(filename_without_extension)
	print ("Found wav file: " + str(wavfile))

	
	## Convert the wavs to mp3
	#title
	title = notes[0] #use the 'first' line of the .LST file
	if "Our Top Ten" not in title:
		title = "Our Top Ten - " + title
		
	#mp3 filename - created from a prefix set above (i.e. show name), a counter, a timestamp and .mp3 
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	#mp3filename = fileprefix + "_" + str(i) + "_" + st + ".mp3"
	mp3filename = fileprefix + "_" + filename_without_extension + "_Archived_" + st + ".mp3"
	print(mp3filename)
	
	#More mp3 tags, album artist and comments
	album_artist = notes[-1].strip() #last item should be the presenter for One to One NB Album artist is a non standardized ID3 tag
	#notes.pop(0) #removes the first item from the list which we have already used for the title
	comment = ', '.join(notes) #uses rest of list items text for the comment
	
	#Run the command to make the mp3 using lame
	cmd = 'lame --preset standard --tt "{}" --tl "{}" --ta "{}" --tv TPE2="{}" --tc "{}" {} {} '.format(title, album, artist, album_artist, comment, wavfile, mp3filename) #wavfile is input, mp3filename is output
	subprocess.call(cmd, shell=True)
	return mp3filename
	

def moveFiles (file, basepath, new_dir):
	os.rename(basepath + '/' + file, basepath + new_dir + file)
	print("Moving " + file)

#Get a list of the files we want to extract - orderd by filename
OurFiles = sorted(listdir("files"))
print (len(OurFiles))

#Loop through the files
for ourfile in OurFiles:
	print (ourfile)
	#Extract the files from the zip
	unzipfile(ourfile)
	#Create an mp3 file using extracted audio and data
	mp3 = create_mp3(ourfile, album, artist)
	moveFiles (mp3, basepath, destination_directory)
	moveFiles (ourfile, basepath + "/files", "/converted_zip/")
	#raise SystemExit()



"""

#Now they are extracted we want to find all the wavs and their corresponding .LST files
extractedFiles = listdir("extracted")


##Get the data from the .LST files
listFiles =[]

for file in extractedFiles:
	if file.endswith(".LST"):
		listFiles.append(file)

print(listFiles)

splitter = "      | - "
i=1

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
	#NB .LST file may not have the same sort of name as the wav file - we can have lowercase myr and wav
	filename_without_extension = splitext(file)[0]
	wavfile = "extracted/" + filename_without_extension + ".WAV"
	# we should check this file exists  if not we ..
	
	## Convert the wavs to mp3	
	title = notes[0] #use the 'first' line of the .LST file
	if "One to One" not in title:
		title = "One to One - " + title
	#mp3 filename - created from a prefix set above (i.e. show name), a counter, a timestamp and .mp3 
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
	#mp3filename = fileprefix + "_" + str(i) + "_" + st + ".mp3"
	mp3filename = fileprefix + "_" + filename_without_extension + "_Archived_" + st + ".mp3"
	print(mp3filename)
		
	album_artist = notes[-1].strip() #last item should be the presenter for One to One NB Album artist is a non standardized ID3 tag
	notes.pop(0) #removes the first item from the list which we have already used for the title
	comment = ', '.join(notes) #uses rest of list items text for the comment
	
	#Run the command to make the mp3 using lame
	cmd = 'lame --preset standard --tt "{}" --tl "{}" --ta "{}" --tv TPE2="{}" --tc "{}" {} {} '.format(title, album, artist, album_artist, comment, wavfile, mp3filename) #wavfile is input, mp3filename is output
	subprocess.call(cmd, shell=True)
	i +=1
"""

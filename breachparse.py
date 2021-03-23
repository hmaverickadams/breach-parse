#!/usr/bin/env python3

import sys
import os

# Very simple recusive function to count the number of non-hidden files in the specified directory structure
def countFiles(directory):
	return((len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]))+
		sum(map(countFiles, ([os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and d[0] != "."]))))

def progressBar(fileCount, totalFiles):
	progress = int((fileCount * 100 / totalFiles * 100) / 100)
	done = int((progress * 4) / 10)
	left = 40 - done
	print(" Progress: ["+"#"*progress+left*"-"+ "]", end="\r")

if(len(sys.argv) < 3):
	print("Breach-Parse v2: A Breached Domain Parsing Tool by Heath Adams and Clark Kevin")
	print("")
	print("Usage: ./breachparse.py <domain to search> <file to output> [breach data location]")
	print("Example: ./breachparse.py @gmail.com gmail.txt")
	print('Example: ./breachparse.py @gmail.com gmail.txt "~/Downloads/BreachCompilation/data"')
	print("You only need to specify [breach data location] if its not in the expected location (/opt/breach-parse/BreachCompilation/data)")
	print("")
	print('For multiple domains: ./breachparse.py "<domain to search>|<domain to search>" <file to output>')
	print('Example: ./breachparse.py "@gmail.com|@yahoo.com" multiple.txt')
	exit(1)
elif(len(sys.argv) > 5 ):
	print('You supplied more than 3 arguments, make sure to double quote your strings:')
	print('Example: ./breachparse.py @gmail.com gmail.txt "~/Downloads/Temp Files/BreachCompilation"')
	exit(1)

# assume default location
breachDataLocation="/opt/breach-parse/BreachCompilation/data"

# check if BreachCompilation was specified to be somewhere else
if(len(sys.argv) == 4 ):
	if(os.path.isdir(sys.argv[3])):
		breachDataLocation=sys.argv[3]
	else:
		print("Could not find a directory at "+sys.argv[3])
		print('Pass the BreachCompilation/data directory as the third argument')
		print('Example: ./breachparse.py @gmail.com gmail.txt "~/Downloads/BreachCompilation/data"')
		exit(1)
else:
	if not(os.path.isdir(breachDataLocation)):
		print("Could not find a directory at "+breachDataLocation)
		print('Put the breached password list there or specify the location of the BreachCompilation/data as the third argument')
		print('Example: ./breachparse.py @gmail.com gmail.txt "~/Downloads/BreachCompilation/data"')
		exit(1)

# set output filenames
fullfile = sys.argv[2]
fbname = fullfile.split("/")[-1].split(".")[0]
master = fbname+"-master.txt"
users = fbname+"-users.txt"
passwords = fbname+"-passwords.txt"

totalFiles = countFiles(breachDataLocation)
fileCount = 0
domains = sys.argv[1].split('|')
masterfd = open(master, "w")
usersfd = open(users, "w")
passwordsfd = open(passwords, "w")

for osdir, subdirs, files in os.walk(breachDataLocation):
	for f in files:
		with open((os.path.join(osdir, f)), "r", encoding='latin-1') as fd:
			fileCount += 1
			progressBar(fileCount, totalFiles)
			for line in fd:
				for domain in domains:
					if(domain in line):
						try:
							masterfd.write(line)
							usersfd.write(line.split(":")[0]+"\n")
							passwordsfd.write(line[line.find(":")+1:])
						except:
							# This usually means the delimeter was not a colon. Could be a semicolon or pipe in some cases
							# Just have the script put the whole line in the master file and let the operator sort it out
							pass # So many delimeters, not enough time



print("")
print("Files written to the current directory:")
print("		"+master)
print("		"+users)
print("		"+passwords)

import os, sys, shlex
from data.powers import name_filter as nf

names = []
numfolders = 1

for subdir, dirs, files in os.walk(sys.argv[1]): # for target dir and subdirs
	
	print('folder #'+str(numfolders))
	
	for file in files:

		if file.endswith('.cohdemo'): # only on demos
			
			demoname = os.path.join(subdir, file) # full path
			numnames, linecount = 0, 0 # reset counts for each file

			with open(demoname,'r') as fp: # open the demo
				line = shlex.split(fp.readline().replace('\\','').replace('\'','')) # split line to array

				while (line and linecount < 30000 and numnames < 16):
					if line[2] == 'NEW' and line[3] not in nf:
						numnames += 1 # number of names in a match
						if line[3] not in names:
							names.append(line[3]) # all names
					
					line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
					linecount += 1
	numfolders += 1

f = open("allnames.txt", "w")
for name in names:
	f.write('\''+name+'\':,\n')
f.close()

import csv

namedict = {}

with open('names.csv', mode='r') as names:
	reader = csv.reader(names)
	# with open('namesdict.csv', mode='w') as dictfile:
	for row in reader:
		namedict[row[0]] = row[1:]
		# for i in range(len(row)):
		#  	namedict[row[0]] += row[i]

for k, v in namedict.items():
	v = [value for value in v if value != '']
	print("\""+k+"\":"+str(v)+",")
# print(namedict)


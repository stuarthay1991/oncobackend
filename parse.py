#Data clean

import preprocessing as prep
prep.moveTo(prep.ndatadir)
infile = open((prep.objects[1]+".pgr.csv.clean"), "r")
colfile = open((prep.objects[1]+".columns"), "r")

rawcol = next(colfile)
rawcol = rawcol.rstrip()
rawcol = rawcol.split(",")

coldict = {}

try:
	while(True):
		line = next(infile)
		line = line.rstrip()
		line = line.split("#")
		for i in range(1, len(line)):
			try:
				coldict[rawcol[i]].append(line[i])
			except:
				coldict[rawcol[i]] = []
except:
	print("Done")

for i in coldict:
	coldict[i] = list(set(coldict[i]))

for i in coldict:
	f = open(("Columns/"+i+".txt"), "w")
	tofile = "#".join(coldict[i]) + "\n"
	f.write(tofile)
	f.close()

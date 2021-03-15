#Preprocessing

import sys, os, numpy

objects = sys.argv
rootdir = "/Users/stuarthay/Desktop/CCHMC/ONCO"
datadir = rootdir + "/dev/data"
testingdatadir = datadir + "/testingdata"
ndatadir = datadir + "/NathanData"

def moveTo(path):
    os.chdir(path)

def findSampleIndsWriteColFile(infile, outfile, delimiter="\t"):
    ret_arr = []
    line = next(infile)
    line = line.rstrip()
    line = line.split(delimiter)
    print(("COL NUM = " + str(len(line))))
    newline = []
    for i in line:
        i = i.replace(" ", "_")
        newline.append(i)
    lineToCsv = ",".join(newline)
    outfile.write(lineToCsv)
    outfile.close()
    for index in range(len(line)):
        if(line[index][-4:] == ".bed"):
            ret_arr.append(index)
    return ret_arr

def loopThroughFile(infile, flag, sampleinds="", outfile="", filemaxcol=0, filemincol=0):
    if(flag == "stat"):
        ret_val = {"data1": []}
    else:
        ret_val = {"data1": []}
    try:
        while(True):
            line = next(infile)
            if(flag == "stat"):
                ret_val["data1"].append(findRowSplicingStats(line))
            if(flag == "clean"):
                corrected_line = fillInRowSplicingValues(line, sampleinds, filemaxcol, filemincol)
                outfile.write(corrected_line)
                outfile.write("\n")
        return ret_val
    except:
        print("BREAK")
        infile.close()
        return ret_val

def printSpecificLine(infile, condition, prop):
    try:
        while(True):
            line = next(infile)
            line = line.rstrip()
            line = line.split("\t")
            if(condition == "length"):
                if(len(line) == prop):
                    print(line)
                    return
    except:
        return

def findRowSplicingStats(line):
    line = line.rstrip()
    line = line.split("\t")
    return len(line)

def fillInRowSplicingValues(line, inds, filemaxcol, filemincol):
    line = line.rstrip()
    line = line.split("\t")
    total_vals = len(line)
    givenvals = []
    for i in inds:
        if(i >= total_vals):
            break
        if(line[i] != ""):
            givenvals.append(float(line[i]))
    working_mean = numpy.median(givenvals)
    working_mean = round(working_mean, 2)
    correct_line = []
    for i in range(filemaxcol):
        if(i >= total_vals):
            correct_line.append("0")
        elif(line[i] == ""):
            if(i < inds[0]):
                correct_line.append("NA")
            else:
                correct_line.append("0")
        else:
            try:
                okl = float(line[i]) - working_mean
                okl = round(okl, 2)
                okl = str(okl)
                correct_line.append(okl)
            except:
                correct_line.append(line[i])
    correct_line = "#".join(correct_line)
    if(len(correct_line.split("#")) != filemaxcol):
        print(len(correct_line.split("#")))
    return correct_line    

def findFileLength(infile):
    starting_num = 0
    try:
        while(True):
            line = next(infile)
            starting_num += 1
    except:
        return starting_num
    
def metaSet(infile, outfile, colfile, delimiter="\t"):
    ret_arr = []
    line = next(infile)
    line = line.rstrip()
    line = line.split(delimiter)
    print(("COL NUM = " + str(len(line))))
    truelength = len(line)
    lineToCsv = ",".join(line)
    colfile.write(lineToCsv)
    colfile.close()
    try:
        while(True):
            line = next(infile)
            line = line.rstrip()
            line = line.split(delimiter)
            for i in range(truelength):
                try:
                    if(len(line[i]) == 0):
                        outfile.write("NA")
                    else:
                        outfile.write(line[i])
                    if(i != (truelength-1)):
                        outfile.write("#")
                except:
                    outfile.write("NA")
                    if(i != (truelength-1)):
                        outfile.write("#")
            outfile.write("\n")
        outfile.close()
    except:
        outfile.close()
        return

def removeMiss(infile, colfile, outfile, delimiter="#"):
    col_match = next(colfile)
    col_match = col_match.rstrip()
    col_match = col_match.split(",")
    try:
        while(True):
            line = next(infile)
            e_line = line.rstrip()
            e_line = e_line.split(delimiter)
            sample = e_line[0] + ".bed"
            for i in col_match:
                if(i == sample):
                    outfile.write(line)
                    break
    except:
        return
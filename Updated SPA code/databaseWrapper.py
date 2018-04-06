import csv
import re
import numpy as np

class Process:

    def __init__(self, name):
        allProcesses = open('allProcesses.txt', 'r')
        self.pname = ""
        self.inputs = []
        self.outputs = []
        found = 0

        # Search for process name and add inputs/outputs with their amounts
        for line in allProcesses:
            if name in line:
                self.pname = name
                found = 1
            if found == 1:
                if line != "\n":
                    nameIndex = line.index("$")-1
                    amtIndex = line.index("*")+1
                    if "$input: True" in line:
                        # append input
                        self.inputs.append([line[0:nameIndex],line[amtIndex:-1]])
                        print("added input: "+line[0:nameIndex]+" "+line[amtIndex:-1])
                    elif "$input: False" in line:
                        # append output
                        self.outputs.append([line[0:nameIndex],line[amtIndex:-1]])
                        print("added output: "+line[0:nameIndex]+" "+line[amtIndex:-1])
                elif line == "\n":
                    break
        allProcesses.close()

    # returns the mass of the name in the process
    def mass(self,name):
        for i in self.inputs:
            if i[0] == name:
                return i[1]
        for o in self.outputs:
            if 0[0] == name:
                return o[1]

    # returns name and amt of inputs with name in it 
    def input(self, name):
        results = []
        for i in self.inputs:
            if name in i[0]:
                results.append(i)
        return results

    # returns list of inputs
    def allInputs(self):
        return self.inputs
    
    # returns list of outputs
    def allOutputs(self):
        return self.outputs
    
    # returns name and amt of outputs with name in it 
    def output(self, name):
        results = []
        for o in self.outputs:
            if name in o[0]:
                results.append(o)
        return results

    # returns the name of the process
    def name(self):
        return self.pname

    
    # returns the top 5 likely outputs for the NAICS code passed in 
    def top5Outputs(self, code):
        naicsDescrs = findNAICS(code)
        scores = []
        for name in self.outputs:
            score = compareNames(name[0],naicsDescrs)
            scores.append([name[0],score,name[1]])
        top5 = []
        numOutputs = len(scores)
        for x in xrange(numOutputs):
            top = topScore(scores)
            scores.remove(top)
            top5.append(top)
        if len(top5) > 5:
            top5 = top5[0:5]
        return top5

    
    # returns the top 5 likely inputs for the NAICS code passed in 
    def top5Inputs(self, code):
        naicsDescrs = findNAICS(code)
        scores = []
        for name in self.inputs:
            score = compareNames(name[0],naicsDescrs)
            scores.append([name[0],score,name[1]])
        top5 = []
        numOutputs = len(scores)
        for x in xrange(numOutputs):
            top = topScore(scores)
            scores.remove(top)
            top5.append(top)
        if len(top5) > 5:
            top5 = top5[0:5]
        return top5


# returns the top score
def topScore(scores):
    top = 0
    index = 0
    i = 0
    for score in scores:
        if score[1] > top:
            top = score[1]
            index = i
        i += 1
    return scores[index]
    
# gives a score on how closely the name relates to the NAICS code
def compareNames(name, naicsDescrs):
    score = 0
    for descr in naicsDescrs:
        naicsWords = re.findall(r"[\w']+",descr)
        for naicsWord in naicsWords:
            nameWords = re.findall(r"[\w']+",name)
            for nameWord in nameWords:
                if nameWord == naicsWord:
                    score += 1
    return score

# function to return list of descriptions for NAICS code passed in   
def findNAICS(code):
    list = []
    code = str(code)
    with open("2017_NAICS_Cross_References.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
    with open("2017_NAICS_Descriptions.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
                list.append(row[2])
    with open("2017_NAICS_Index_File.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
    return list

def top5Processes(self, desc):
    processNames =  open("processNames.txt",'r')
    scores = []
    for line in processNames:
        score = compareNames(line,desc)
        scores.append([line,score])
    top5 = []
    numOutputs = len(scores)
    for x in xrange(numOutputs):
        top = topScore(scores)
        scores.remove(top)
        top5.append(top)
    if len(top5) > 5:
        top5 = top5[0:5]
    return top5

# examples     
p1 = Process("Metal composite material (MCM) panel, at plant")
'''
print("name of process:")
print(p1.name())

print("all inputs:")
print(p1.allInputs())

print("all outputs:")
print(p1.allOutputs())

print("inputs with CUTOFF:")
print(p1.input("CUTOFF"))

print("mass of CUTOFF Steel cast part (machined):")
print(p1.mass("CUTOFF Steel cast part (machined)"))

result = p1.top5Inputs(336310)
print(result)


with open("myfile4.txt","r") as f:
    lines = f.readlines()
    model = lines[1].lstrip()
    print(model)
    #matrix = np.array([)
    for line in lines[2:]:
        value1 = line[:9]
        noValue1 = line[9:]
        f = len(noValue1) - len(noValue1.lstrip())
        noWhite = noValue1[f:]
        endNumbers = noWhite.find(" ")
        numbers = noWhite[:endNumbers].split("----")
        print(value1)
        print(numbers)
        for x in reversed(numbers[:-1]):
            naics = x #hard coded for now
            top = p1.top5Inputs(naics)
            print(top)
'''

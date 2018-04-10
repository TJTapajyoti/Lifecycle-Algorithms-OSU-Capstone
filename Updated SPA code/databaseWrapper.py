import csv
import re

class Process:

    def __init__(self, name):
        allProcesses = open('allProcesses.txt', 'r')
        lines = allProcesses.readlines()
        self.pname = ""
        self.inputs = []
        self.outputs = []
        process = ""
        # Search for process name and add inputs/outputs with their amounts
        i = 1
        while self.pname == "":
            line = lines[i]
            # check if process name matches
            if name in line:
                # get inputs/outputs
                self.pname = name
                i += 1
                while lines[i] != "\n":
                    puts = lines[i]
                    i += 1
                    nameIndex = puts.index("$")-1
                    amtIndex = puts.index("*")+1
                    if "$input: True" in puts:
                        # input
                        self.inputs.append([puts[0:nameIndex],puts[amtIndex:-1]])
                        print("added input: "+puts[0:nameIndex]+" "+puts[amtIndex:-1])
                    elif "$input: False" in puts:
                        # output
                        self.outputs.append([puts[0:nameIndex],puts[amtIndex:-1]])
                        print("added output: "+puts[0:nameIndex]+" "+puts[amtIndex:-1])
            else:
                while lines[i] != "\n":
                    i += 1
            i += 1
        allProcesses.close()

    # returns the mass of the name in the process
    def mass(self,name):
        mass = 0
        inputsOutputs = self.inputs + self.outputs
        for i in inputsOutputs:
            if i[0] == name:
                print(i[0])
                print(name)
                space = i[1].index(" ")
                mass = float(i[1][:space])
        return mass
    
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

    # returns the value of the carbonDioxide output
    def carbonDioxide(self):
        co2 = ""
        for i in self.outputs:
            if "Carbon dioxide, fossil " in i[0]:
                co2 = i[1]
        return co2
    '''
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
    '''
    
    # returns the top 5 likely inputs for the NAICS code passed in 
    def top5Inputs(self, code):
        naicsDescrs = NAICSdescription(code)
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
                if nameWord.lower() == naicsWord.lower():
                    score += 1
    return score

# function to return list of descriptions for NAICS code passed in   
def NAICSdescription(code):
    list = []
    code = str(code)
    with open("2017_NAICS_Cross_References.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
        f.close()
    with open("2017_NAICS_Descriptions.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
                list.append(row[2])
        f.close()
    with open("2017_NAICS_Index_File.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
        f.close()
    return list

processNames =  open("processNames.txt",'r')
# returns the top 5 most likely process names from database, based on description passed in
def top5Processes(desc):
    scores = []
    for line in processNames:
        score = compareNames(line,desc)
        if score > 0:
            scores.append([line[:-1],score])
    top5 = []
    numOutputs = len(scores)
    for x in xrange(numOutputs):
        top = topScore(scores)
        scores.remove(top)
        top5.append(top[0])
    if len(top5) > 5:
        top5 = top5[0:5]
    return top5

# examples     
'''
p1 = Process("Transport, single unit truck, short-haul, diesel powered, South")
print(p1.carbonDioxide())

print("name of process:")
print(p1.name())

print("all inputs:")
print(p1.allInputs())

print("all outputs:")
print(p1.mass("Carbon dioxide, fossil "))

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
            naics = 21113 #hard coded for now
            top = p1.top5Inputs(naics)
            print(top)
'''

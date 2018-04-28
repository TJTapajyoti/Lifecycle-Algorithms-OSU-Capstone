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
                    unitIndex = puts.index("!")
                    try:
                        unit = puts[unitIndex+1:-1]
                    except:
                        unit = " "
                    if "$input: True" in puts:
                        # input
                        self.inputs.append([puts[0:nameIndex],puts[amtIndex:unitIndex],unit])
                        #print("added input: "+puts[0:nameIndex]+" "+puts[amtIndex:unitIndex]+unit)
                    elif "$input: False" in puts:
                        # output
                        self.outputs.append([puts[0:nameIndex],puts[amtIndex:unitIndex],unit])
                        #print("added output: "+puts[0:nameIndex]+" "+puts[amtIndex:-1])
            else:
                while lines[i] != "\n":
                    i += 1
            i += 1
        allProcesses.close()

    # returns the value of the carbonDioxide output
    def carbonDioxide(self):
        co2 = 0
        for i in self.outputs:
            if "Carbon dioxide, fossil " in i[0]:
                co2 = float(i[1])
        return co2

    # returns the top 5 likely inputs for the NAICS code passed in 
    def top5Inputs(self, description, searchType):
        scores = []
        for name in self.inputs:
            if searchType == 1:
                score = compareNames(name[0],description)
            elif searchType == 2:
                score = compareNames2(name[0],description)                
            if score > 0:
                scores.append([name[0],score,name[1],name[2]])
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
def compareNames(name, descrs):
    score = 0
    for descr in descrs:
        naicsWords = re.findall(r"[\w']+",descr)
        for naicsWord in naicsWords:
            nameWords = re.findall(r"[\w']+",name)
            for nameWord in nameWords:
                if naicsWord.lower() in nameWord.lower():
                    score += 1
    return score

def compareNames2(name, descrs):
    score = 0
    for descr in descrs:
        naicsWords = re.findall(r"[\w']+",descr)
        for naicsWord in naicsWords:
            nameWords = re.findall(r"[\w']+",name)
            for nameWord in nameWords:
                if naicsWord.lower() == nameWord.lower():
                    score += 1
    return score
'''
# function to return list of descriptions for NAICS code passed in   
def NAICSdescription(code):
    list1 = []
    code = str(code)
    with open("2017_NAICS_Cross_References.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list1.append(row[1])
        f.close()
    with open("2017_NAICS_Descriptions.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list1.append(row[1])
                list1.append(row[2])
        f.close()
    with open("2017_NAICS_Index_File.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list1.append(row[1])
        f.close()
    return list1
'''

# returns the top 5 most likely process names from database, based on description passed in
def top5Processes(desc,searchType):
    processNames = open("processNames.txt",'r')
    scores = []
    for line in processNames:
        name = line.index("$")
        if searchType == 1:
            score = compareNames(line[:name],desc)
        elif searchType == 2:
            score = compareNames2(line[:name],desc)
        if score > 0:
            unit = line.index("!")
            scores.append([line[:name],score,line[name+1:unit],line[unit+1:-1]])
    top5 = []
    for x in xrange(len(scores)):
        top = topScore(scores)
        #print(top)
        scores.remove(top)
        top5.append([top[0],top[2],top[3]])
    if len(top5) > 5:
        top5 = top5[0:5]
    processNames.close()
    return top5

# examples

#print(top5Processes(["chemical"]))
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

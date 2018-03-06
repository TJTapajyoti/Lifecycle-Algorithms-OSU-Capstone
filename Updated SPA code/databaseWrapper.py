
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

# examples     
p1 = Process("Metal composite material (MCM) panel, at plant")
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





class Process:

    def __init__(self, name):
        allProcesses = open('allProcesses.txt', 'r')
        self.pname = ""
        self.inputs = []
        self.outputs = []
        found = 0

        # Search for process name and add inputs/outputs 
        for line in allProcesses:
            if name in line:
                self.pname = name
                found = 1
                print(line)
            if found == 1:
                if line != "\n":
                    index = line.index("$")-1
                    if "$input: True" in line:
                        # append input
                        self.inputs.append(line[0:index])
                        print("added input: "+line[0:index])
                    elif "$input: False" in line:
                        # append output
                        self.outputs.append(line[0:index])
                        print("added output: "+line[0:index])
        allProcesses.close()

    # returns the mass of the name in the process
    def mass(self,name):
        return 0

    # returns list of inputs with name in it 
    def input(self, name):
        results = []
        for i in self.inputs:
            if name in i:
                results.append(i)
        return results

    # returns list of inputs
    def inputs(self):
        return self.inputs
    
    # returns list of outputs
    def outputs(self):
        return self.outputs
    
    # returns list of outputs with name in it
    def output(self, name):
        results = []
        for o in self.outputs:
            if name in o:
                results.append(i)
        return results
    def name(self):
        return self.pname
    
p1 = Process("Transport, transit bus, diesel powered, Northeast")
print(p1.inputs)
print(p1.outputs)

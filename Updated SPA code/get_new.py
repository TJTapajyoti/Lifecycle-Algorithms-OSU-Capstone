processNames = open('processNames.txt','w')

with open('allProcesses.txt') as f:
	prev = 'a'
	for line in f:
		if prev == '\n':
                        end = line.index("$")-1
			processNames.write(line[:end]+"\n")
			prev = line
		else:
			prev = line


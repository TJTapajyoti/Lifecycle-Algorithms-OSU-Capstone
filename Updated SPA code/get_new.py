processNames = open('processNames.txt','w')

with open('allProcesses.txt') as f:
	prev = 'a'
	for line in f:
		if prev == '\n':
                        name = line.index("$")-1
                        amount = line.index("*")+1
                        unit = line.index("!")
			processNames.write(line[:name]+"$"+line[amount:unit]+"!"+line[unit+1:])
			prev = line
		else:
			prev = line


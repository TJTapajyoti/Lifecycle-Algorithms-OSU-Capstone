with open('allProcesses.txt') as f:
	prev = 'a'
	for line in f:
		if prev == '\n':
			print(line)
			prev = line
		else:
			prev = line


#!/usr/bin/python
import json
import os

output = open("allProcesses.txt", "w")
for fn in os.listdir('.'):
    #print(str(fn))	
    if fn.endswith(".json"):
        with open(fn, 'r') as f:
            d = json.load(f)
            output.write("\n")
            for e in d['exchanges']:
                output.write(e['flow']['name'].encode('utf-8')+' $')
                output.write('input: '+str(e['input'])+' *')
                output.write(str(e['amount'])+'!')
                try:
                    output.write(e["unit"]['name']+'\n')
                except:
                    print("no unit for "+e['flow']['name'].encode('utf-8'))
                    output.write("\n")

import python_wrapper as p
'''
a = p.Model_Generator()
a.add_process_output('A03', 25, 1.5)
a.add_process_input('A01', 10.074, 3.0)
a.add_process_input('A02', 8.0592, 2.5)
a.add_environmental_impact(7.5)
a.add_v('v.csv')
a.add_u('u.csv')
a.add_b('b.csv')
a.add_codes('codes.csv')
a.run_spa('A03')
'''
import csv

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
    with open("2017_NAICS_Index_File.csv",'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == code:
                list.append(row[1])
    return list



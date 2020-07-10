import numpy as np 
import argparse
import json

parser = argparse.ArgumentParser(
        description="""A tool to help write columns labels for UK Biobank data""", add_help=True
    )

parser.add_argument('--columnsFile', metavar='e.g. analysisCols.txt', type=str, default = "analysisCols.txt", 
                            help="""The text file listing columns to include
                            """ )

args = parser.parse_args()


with open(args.columnsFile,
 'r') as file:
    data = file.readlines()
    data = [i.split('#', 1)[0].split(' ', 1)[0].split('\n', 1)[0] for i in data]
    data = [i for i in data if i != '' ]

d = "{"
for i in data[0:-1]: 
    d += '"' + i + '-0.0":{} , '
d += '"' + data[-1] + '-0.0":{}}'
d = eval(d)

with open("columns.json", "w") as f: 
    json.dump(d,f )


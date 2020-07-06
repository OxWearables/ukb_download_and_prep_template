import numpy as np 
import argparse

parser = argparse.ArgumentParser(
        description="""A tool to help write columns labels for UK Biobank data""", add_help=True
    )

parser.add_argument('--columns_text_file', metavar='e.g. analysisCols.txt', type=str, default = "analysisCols.txt", 
                            help="""The text file listing columns to include
                            """ )

args = parser.parse_args()


with open(args.columns_text_file,
 'r') as file:
    data = file.readlines()
    data = [i.split('#', 1)[0].split(' ', 1)[0].split('\n', 1)[0] for i in data]
    data = [i for i in data if i != '' ]
w = open("columns.py", "w" )
w.write("import numpy as np \nCOLUMNS = {")
for i in data[0:-1]: 
    w.write("'" + i + "-0.0':{},")
w.write("'" + data[-1] + "-0.0':{}")
w.write("}")


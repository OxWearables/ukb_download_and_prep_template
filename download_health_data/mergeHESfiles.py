import argparse
import os
import pandas as pd
import sys

def str2bool(v):
    """
    Used to parse true/false values from the command line. E.g. "True" -> True
    """
    return v.lower() in ("yes", "true", "t", "1")

parser = argparse.ArgumentParser(
        description="""Merge UKB hesin, hesin_diag[9/10] tables and write
        master csv file to support analysis""", add_help=True
    )
parser.add_argument('hesinTXT', metavar='hesinTXT', type=str, help="""
path of .txt file from hesin table (admission information) 
""")
parser.add_argument('diagTXT', metavar='diagTXT', type=str, help="""
.tsv file from hesin_diag (ICD10 diagnosis codes, primary and secondary) 
""")
parser.add_argument('masterCSV', metavar='masterCSV', type=str, help="""
output .csv master file for subsequent health analyses
""")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit()

# load data
print('loading data')
hesin = pd.read_csv(args.hesinTXT, sep='\t')
hesin_diag = pd.read_csv(args.diagTXT, sep='\t')

print('merging datasets together')
#add secondary ICD 10 codes
hesin_all = hesin.set_index(['eid','ins_index']).join( \
        hesin_diag.set_index(['eid','ins_index']), rsuffix='_ICD')

# write new master hes file
print('writing master CSV file (this will take a few minutes, please be patient)')
hesin_all.to_csv(args.masterCSV)
print('finished writing CSV file')

# delete original input files as they are no longer needed
print('deleting original input files that are no longer needed')
os.remove(args.hesinTXT)
os.remove(args.diagTXT)

print('processing finished')

import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import numpy as np
import os
import pandas as pd
import scipy.stats
from subprocess import call
import sys

parser = argparse.ArgumentParser(
        description="""Join existing demographic and health data file with new Hospital Episode Statistics data
        		for subsequent health analyses""",
        add_help=False
        )
# required args
parser.add_argument('inCSV', type=str,
        help="""CSV file containing current data
            If the path contains spaces, it must be enclosed in
            quote marks (e.g. "/data/dph.../data sets/")""")
parser.add_argument('hesCSV', type=str, help="hospital episode statistics csv")
parser.add_argument('outCSV', type=str, help="""output for analysis csv""")
parser.add_argument('diseaseJSON', type=str, default="icdGroups.json", help="""target ICD10/ICD9 groups json""")
# parse arguments
if len(sys.argv) < 5:
    parser.print_help()
    sys.exit(-1)
args = parser.parse_args()

'''
Read file of current data
'''
print('read ' + args.inCSV)
dAll = pd.read_csv(args.inCSV)
if ('file.startTime' not in list(dAll.columns)):
    sys.exit('file.startTime needs to be a column of inCSV in order to define incident and prevalent disease.')

dAll['file.startTime'] = pd.to_datetime(dAll['file.startTime'])
dAll = dAll.set_index('eid')

'''
Read HES file
'''
print('read and clean ' + args.hesCSV)
dHES = pd.read_csv(args.hesCSV, parse_dates=['epistart','disdate'])
dHES = dHES[dHES['eid'].isin(dAll.index)] # restrict to participants in dAll

print(len(dHES), 'len dataframe')
diseaseList = json.loads(open(args.diseaseJSON).read())

def cleanHESstr(s):
    return s.strip().replace('&','').replace("'","").replace(' ','-').replace(',','')



print('Finding participants with: ')
dHES.loc[dHES['epistart'].isnull(), 'epistart'] = dHES['disdate']
# first check for any disease history
# outcomeName = 'anyDisease'
# e = dHES[['eid','epistart']]
# outcomePts = e[['epistart']].groupby(e['eid']).min()
# outcomePts.columns = [outcomeName]
# dAll = dAll.join(outcomePts)

# dAll[outcomeName + "-incident"] = 0
# dAll.loc[(dAll[outcomeName] > dAll['file.startTime']) & \
#        (~dAll[outcomeName].isnull()), outcomeName + '-incident'] = 1
# dAll[outcomeName + "-prevalent"] = 0
# dAll.loc[(dAll[outcomeName] <= dAll['file.startTime']) & \
#        (~dAll[outcomeName].isnull()), outcomeName + '-prevalent'] = 1
# print(outcomeName, ', n = ', len(dAll[~dAll[outcomeName].isnull()]))
# finally check for history of specific diseases
for outcome in diseaseList:
   outcomeName = cleanHESstr(outcome['disease'])
   e = dHES[['eid','epistart']]\
          [(dHES['diag_icd10'].str.contains(outcome['icd10'], na=False)) | \
           (dHES['diag_icd9'].str.contains(outcome['icd9'], na=False)) ]
   outcomePts = e[['epistart']].groupby(e['eid']).min()
   outcomePts.columns = [outcomeName]
   dAll = dAll.join(outcomePts)
   dAll[outcomeName + "-incident"] = 0
   dAll.loc[(dAll[outcomeName] > dAll['file.startTime']) & \
           (~dAll[outcomeName].isnull()), outcomeName + '-incident'] = 1
   dAll[outcomeName + "-prevalent"] = 0
   dAll.loc[(dAll[outcomeName] <= dAll['file.startTime']) & \
           (~dAll[outcomeName].isnull()), outcomeName + '-prevalent'] = 1
   print(outcomeName, ', n = ', len(dAll[~dAll[outcomeName].isnull()])) 

'''
Write final output file...
'''

print('write final cleaned file to ' + args.outCSV)
dAll.to_csv(args.outCSV)
print('finished')
import argparse
import pandas as pd
import sys

def str2bool(v):
    """
    Used to parse true/false values from the command line. E.g. "True" -> True
    """
    return v.lower() in ("yes", "true", "t", "1")

parser = argparse.ArgumentParser(
    description="""Select only participants with accelerometer data
    i.e. having valid calibration coefficients""", add_help=True
    )
parser.add_argument('inputUKBcsv', metavar='inputUKBcsv', type=str, help="""
    path of file with calibration coefficients cols for all UKB participants 
    """)
parser.add_argument('outCsv', metavar='outCsv', type=str, help="""
    path of output csv file with calibration coefficients for acc participants
    """)
parser.add_argument('--outDownloadTxt', metavar='outDownloadTxt', type=str,
    default="download.txt", help=""" path of output txt file with download cmds 
    for acc files""")
parser.add_argument('--splitOutput', metavar='True/False', default=True,
    type=str2bool, help="""split output into 5k chunks? (default :
    %(default)s)""")
parser.add_argument('--subfolderSize', default=10000,
    type=int, help="""Num files in subfolder, if splitting (default :
    %(default)s)""")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit()

d = pd.read_csv(args.inputUKBcsv)
colHeads={'90161-0.0':'xOff'}
colHeads['90162-0.0'] = 'yOff'
colHeads['90163-0.0'] = 'zOff'
colHeads['90164-0.0'] = 'xSlope'
colHeads['90165-0.0'] = 'ySlope'
colHeads['90166-0.0'] = 'zSlope'
colHeads['90167-0.0'] = 'xTemp'
colHeads['90168-0.0'] = 'yTemp'
colHeads['90169-0.0'] = 'zTemp'
colHeads['90170-0.0'] = 'meanTemp'
d.columns = d.rename(columns=colHeads).columns
d['fileName'] = d['eid']
d['calOffset'] = d['xOff'].astype(str) + ' ' + d['yOff'].astype(str) + ' ' \
        + d['zOff'].astype(str)
d['calSlope'] = d['xSlope'].astype(str) + ' ' + d['ySlope'].astype(str) + ' ' \
        + d['zSlope'].astype(str)
d['calTemp'] = d['xTemp'].astype(str) + ' ' + d['yTemp'].astype(str) + ' ' \
        + d['zTemp'].astype(str)
outCols = ['fileName', 'calOffset', 'calSlope', 'calTemp', 'meanTemp']

# write download commands
# /bm1/datasets/uk-biobank/terry15856/participantInfo/ukbfetch -e3946792 
# -d90001_0_0 -a/bm1/datasets/uk-biobank/terry15856/participantInfo/k15856.key;
# gzip 3946792_90001_0_0.cwa;
ukbfetch = "/bm1/datasets/uk-biobank/terry15856/participantInfo/ukbfetch"
dataset = "90001_0_0"
key = "/bm1/datasets/uk-biobank/terry15856/participantInfo/k15856.key"
d['download'] = ukbfetch + ' -e' + d['eid'].astype(str) + ' -d' + dataset \
        + ' -a' + key + '; gzip ' + d['eid'].astype(str) + '_' + dataset + '.cwa;'

dNew = d.dropna()
if not args.splitOutput:
    dNew[outCols].to_csv(args.outCsv, index=False)
    dNew['download'].to_csv(args.outDownloadTxt, index=False)
else:
    step = args.subfolderSize
    i = 0
    while i < len(dNew):
        newCsvName = args.outCsv.replace('.csv', '-' + str(i/step) + '.csv')
        dNew[outCols][i:i+step].to_csv(newCsvName, index=False)
    
        newTxtName = args.outDownloadTxt.replace('.txt', '-' + str(i/step) + '.txt')
        dNew['download'][i:i+step].to_csv(newTxtName, index=False)
        i += step

import argparse
import pandas as pd
import sys
from subprocess import call

def str2bool(v):
    """
    Used to parse true/false values from the command line. E.g. "True" -> True
    """
    return v.lower() in ("yes", "true", "t", "1")

parser = argparse.ArgumentParser(
        description="Setup dirs to download participants' accelerometer data",
        add_help=True
    )
parser.add_argument('inCSV', type=str,
        help="CSV with calibration coefficients cols for all UKB participants")
parser.add_argument('outDIR', type=str,
        help="root directory of UKBB study setup folders")
# optional arguments
parser.add_argument('--studyCreationScript', type=str, default="createStudyDir.sh",
        help="path to study creation script (default : %(default)s)")
parser.add_argument('--subfolderSize', default=10000,
        type=int, help="Num files in subfolder (default : %(default)s)")
parser.add_argument('--ukbfetch', type=str, default="./ukbfetch",
        help="Path to ukbfetch (default : %(default)s)")
parser.add_argument('--ukbKey', type=str, default="k9126.key",
        help="Path to ukb key file (default : %(default)s)")
parser.add_argument('--outDownloadTxt', type=str, default="download.txt",
        help="Path of output txt file with download cmds (default : %(default)s)")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit()

# 1. read input CSV, and convert into format for acc analysis
d = pd.read_csv(args.inCSV)
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
fileCols = ['fileName', 'calOffset', 'calSlope', 'calTemp', 'meanTemp']

# 2. only keep participants who have calibration data i.e. who wore the device
d= d.dropna()

# 3. Create data directories
dataset = "90001_0_0"
step = args.subfolderSize
i = 0
while i < len(d):
    # create study subfolder directory
    studyDir = args.outDIR + 'subfolder-' + str(i/step) + '/'
    cmdArgs = ['mkdir', studyDir]
    call(cmdArgs)
    cmdArgs = ['bash', args.studyCreationScript, studyDir]
    call(cmdArgs)

    # update where this file will be located
    d['fileName'][i:i+step] = studyDir + 'rawData/' + \
            d['eid'][i:i+step].astype(str) + '_' + dataset + '.cwa.gz'
    
    # write files.csv for this subdir
    filesCSV = studyDir + "files.csv"
    d[fileCols][i:i+step].to_csv(filesCSV, index=False)
    i += step

# 4.  write download commands
# ./ukbfetch -e3946792 -d90001_0_0 -ak15856.key; gzip 3946792_90001_0_0.cwa;
d['download'] = args.ukbfetch + ' -e' + d['eid'].astype(str) + ' -d' + dataset \
        + ' -a' + args.ukbKey + '; gzip ' + d['eid'].astype(str) + '_' + dataset + '.cwa;' \
        + 'mv ' + d['eid'].astype(str) + '_' + dataset + '.cwa.gz' + ' ' \
        + d['fileName'].astype(str) + ';'

d['download'].to_csv(args.outDownloadTxt, index=False)

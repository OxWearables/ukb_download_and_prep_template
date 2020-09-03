# Relabelling and recoding a participant data `.csv` file 
Your `ukb12345.csv` from the last step looks something like this:

| eid     | 31-0.0 | 34-0.0 | 54-0.0 |   ...
|---------|--------|--------|--------|--------
| 4987419 | 0      | 1944   | 11016  |   ...
| 2898413 | 0      | 1956   | 11009  |   ...
| 1049655 | 1      | 1947   | 11010  |   ...
| 1892589 | 1      | 1941   | 11011  |   ...
| 2449164 | 1      | 1958   | 11010  |   ...

(This is fake data - Any resemblance to real UK Biobank participants is coincidental!)

- The column names are given as field IDs, and you would need to browse https://biobank.ndph.ox.ac.uk/showcase/search.cgi to get their meanings. For example, `31-0.0` is sex, `34-0.0` is year of birth, and `54-0.0` is assessment center. 
- If a field is categorical then its categories are coded e.g. in sex `0` means female and `1` means male, and in assessment center `11010` is Leeds and `11009` is Newcastle. 
- You may have hundreds or thousands of these columns. 

Therefore, the next step towards having ready-to-use data is to filter out some columns and parse the field IDs and categorical codes. (While this can be done manually, the automated tools in this repo aim to make it quicker and easier.)

### Steps

1. Auto-generate a `columns.json` file from the text file of field IDs (in the format used in download_participant_data):
```Bash
  $ python writeColumnsFile.py --columnsFile analysisCols.txt 
 ```
2. Run:
```Bash
$ python filterUKB.py ukb12345.csv -o outputFilename.csv
```
If you want to customise the behaviour or add subsequent columns manually, see [Advanced usage](https://github.com/activityMonitoring/ukb_download_and_prep_template#5-advanced-usage).

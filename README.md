# ukb_download_and_prep_template

Detailed documentation is available [here](https://ukb-download-and-prep-template.readthedocs.io/)

## Quickstart
This usage tutorial assumes you have downloaded and extracted a `.csv` file containing participant data and a `hesin_all.csv` file with health record data from UK Biobank. The [download](https://github.com/activityMonitoring/ukb_download_and_prep_template/download) folder contains guidance on how to download these. 

### 1. Installation 

To use this repo, run: 
  ```Bash
  $ git clone git@github.com:activityMonitoring/ukb_download_and_prep_template
  ```
 
This repo requires `pandas` and `nltk`. If you are using an Anaconda installation of Python, these are included. Otherwise, run: 
  ```Bash
  $ pip install pandas
  $ pip install nltk
  ```

Navigate to the repo: 
  ```Bash
  $ cd ukb_download_and_prep_template
  ```

### 2. Relabelling and recoding a participant data `.csv` file 
You should have a `ukb12345.csv` participant data file which looks something like this:

| eid     | 31-0.0 | 34-0.0 | 54-0.0 |   ...
|---------|--------|--------|--------|--------
| 4987419 | 0      | 1944   | 11016  |   ...
| 2898413 | 0      | 1956   | 11009  |   ...
| 1049655 | 1      | 1947   | 11010  |   ...
| 1892589 | 1      | 1941   | 11011  |   ...
| 2449164 | 1      | 1958   | 11010  |   ...

The next step towards having ready-to-use data is to filter out some columns and parse the field IDs and categorical codes. 
#### Steps

1. Auto-generate a `columns.json` file from the text file of field IDs (in the format used in download_participant_data):
```Bash
  $ python writeColumnsFile.py --columnsFile analysisCols.txt 
 ```
2. Run:
```Bash
$ python filterUKB.py ukb12345.csv -o outputFilename.csv
```

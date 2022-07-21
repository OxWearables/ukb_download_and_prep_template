# ukb_download_and_prep_template

Detailed documentation is available [here](https://ukb-download-and-prep-template.readthedocs.io/).

**WARNING: This template was written to work with data in formats provided directly by UK Biobank via the Showcase or Data Portal (traditional access route). It is unlikely to work correctly with data downloaded from the UKB RAP (new access route). For example, [this bug](https://github.com/OxWearables/ukb_download_and_prep_template/issues/10) has been reported. It should not be used with data downloaded from the RAP without suitable amendment.**

*IMPORTANT*: If you used or are using a version of this repo from before 19.02.2021, an error in date processing may have caused wrongly assigned dates for health outcomes. Please re-download and re-process any data processed with `addNewHES.py`. 

*This is the in-development version and major changes and corrections may be made - use at your own risk! Please share comments, suggestions and errors/bugs found, either directly on the GitHub page or by emailing rosemary.walmsley@gtc.ox.ac.uk*. 

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
### 3. Adding Hospital Episode Statistics on particular diseases
We now add columns on disease diagnoses in hospital. 
You will need: 
 - `hesin_all.csv`: this is a file containing Hospital Episode Statistics data for all participants. 
 - `icdGroups.json`: this is a JSON file containing descriptions of required HES code. 
 - An existing dataset `input.csv` (which might be `outputFilename.csv` from the last section). 
 - If you want to define prevalent and incident disease, `input.csv` should also contain a date column which will be used to define this. 

Then run: 
```
python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column 'name_of_date_column'
```

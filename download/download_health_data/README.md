# Downloading health record data from the UK Biobank database

UK Biobank benefits from passive follow-up via health record linkage.

To understand the available datasets: 
- Here is [a good summary of what health outcomes data exists and pros and cons of using different aspects](http://biobank.ndph.ox.ac.uk/showcase/showcase/docs/HealthOutcomesOverview.pdf) (up-to-date as of Sep 2019).
- Note the [dates for which HES data are available](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=Data_providers_and_dates).

Here, we discuss Hospital Episode Statistics: [ICD9/10 codes](https://www.who.int/classifications/icd/icdonlineversions/en/) from hospital admissions. If you require Operations and Procedures codes or primary care codes, these need to be processed separately. 

## To add new codes to an existing dataset: 

To add new codes to an existing dataset, `/well/doherty/projects/UKBB/HES/hesin_all.csv` contains all HES data, and the script `addnewHES.py` can be used. If `icdGroups.json` is a JSON file containing descriptions of required HES codes (as in the examples in this folder), the usage is as follows: 
```
python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json
 ```
 
**Note:** This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields [40001 and 4002](https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093)). 

## To freshly download HES data (e.g after new releases):

Before downloading any HES data for yourself, you should read the [UK Biobank guide on how to access data](http://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf). If you do this after a new release, please update `hesin_all.csv` in `/well/doherty/projects/UKBB/HES`.  

### Download steps
1. Follow the [UKB guide to access the data portal](http://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf). 
2. It is easiest to download the whole table for the relevant data type (e.g. hesin is required for using all the others, hesin_diag provides diagnosis codes, hesin_oper operation codes).
	- You can do this by putting the name of the data table in the box provided in the Table Download tab. 

	- If you wish to use the data portal, these SQL statements will download all diagnosis codes from hesin_diag and hospital episode information from hesin:
	  ```SQL
	  SELECT eid, ins_index, admidate, disdate, epiend, epistart FROM hesin # then click 'Download'
	  SELECT * FROM hesin_diag # click 'Download'
	  ```
  
3. Join files together to ensure secondary ICD9/10 codes are recorded, then upload as master csv
	  ```Bash
	  # Rename files if necessary to match the names used here

	  # Call python script to merge files together and delete downloaded input files
	  python mergeHESfiles.py ~/Downloads/hesin.txt ~/Downloads/hesin_diag.txt \
	  ~/Downloads/hesin_all.csv

	  # Copy the relevant *.csv files to /..path../participant-info/
	  scp ~/Downloads/hesin_all.csv your_rescomp_username@rescomp.well.ox.ac.uk:/well/doherty/projects/UKBB/participant-info/
	  ```
 


# download_health_data

UK Biobank benefits from passive follow-up via health record linkage.

To understand the available datasets: 
- Here is [a good summary of what health outcomes data exists and pros and cons of using different aspects](http://biobank.ndph.ox.ac.uk/showcase/showcase/docs/HealthOutcomesOverview.pdf) (up-to-date as of Sep 2019).
- Note the [dates for which HES data are available](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=Data_providers_and_dates).

Here, we discuss Hospital Episode Statistics: [ICD9/10 codes](https://www.who.int/classifications/icd/icdonlineversions/en/) from hospital admissions. If you require Operations and Procedures codes or primary care codes, these need to be processed separately. 

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
	  python mergeHESfiles.py ~/Downloads/ukb.txt ~/Downloads/ukb_diag.txt \
	  ~/Downloads/hesin_all.csv

	 
	  ```
 


# ukb_download_and_prep_template
This repository aims to provide a template for the preparation of [UK Biobank](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi) participant and health record data. It is split into sections on: 
 1. Installation 
 2. Extracting participant data to `.csv` format from `.enc_ukb` format
 3. Relabelling and recoding a participant data `.csv` file using Python
 4. Extracting Hospital Episode Statistics on particular diseases
 5. Advanced usage

This folder assumes you have downloaded and extracted a `.enc_ukb` file (participant data) and a `hesin_all.csv` file (health record data) from UK Biobank. The [download](https://github.com/activityMonitoring/ukb_download_and_prep_template/download) folder contains guidance on how to download these. 

A UK Biobank dataset is associated with a numbered application and, within that application, a numbered copy (this is so subsequent additions of variables to the same application can be distinguished). Different applications have access to different sets of variables. Throughout this folder we assume we are using copy number 12345.  

## 1. Installation 

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

## 2. Extracting participant data to `.csv` format from `.enc_ukb` format
To access a particular set of variables in `.csv` format, we extract them from the `12345.enc_ukb` file (which contains all variables in the application for all participants). 

	1. Find the [UK Biobank Data Field IDs](http://biobank.ctsu.ox.ac.uk/crystal/search.cgi) of interest (e.g. [smoking status is 20116](http://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=20116)).
	2. If it is not already there, append this entry to the file `analysisCols.txt`
	3. Extract data to `.csv` format:  

	  ```Bash
	  # CSV
	  $ helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb csv -ianalysisCols.txt
	  # output = path_to_data/ukb12345.csv
	  
	  ```
### Usage notes 
 - These steps can be done in Windows, Linux or MacOS, but the helper files you need will be slightly different (the tools are in helpers/linux_tools for Linux/MacOS and helpers/windows_tools for Windows).
 - This may fail initially because `analysisCols.txt` contains a field ID which is not present in this copy of the dataset. These field IDs should be removed from `analysisCols.txt`. 
 - How long this extraction will take depends on the number of columns you are extracting, but it is not unusual for it to take several hours. If you just want to add a couple of columns, it is quicker to list them in a separate file (e.g. `analysisColsMini.txt`), extract a small `.csv` file and merge with the existing file on participant IDs. 
 -[UK Biobank's guide to accessing the data](https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf) is helpful for queries. 

## 3. Relabelling and recoding a participant data `.csv` file using Python
Your `ukb12345.csv` from the last step looks something like this:

| eid     | 31-0.0 | 34-0.0 | 52-0.0 | 53-0.0     | 54-0.0 |   ...
|---------|--------|--------|--------|------------|--------|--------
| 4937419 | 1      | 1944   | 8      | 2009-01-12 | 11010  |   ...
| 2860412 | 0      | 1951   | 7      | 2008-12-11 | 11009  |   ...
| 1039354 | 0      | 1945   | 12     | 2008-07-28 | 11010  |   ...
| 1592599 | 1      | 1939   | 3      | 2009-02-09 | 11011  |   ...
| 3849156 | 1      | 1958   | 1      | 2009-02-27 | 11016  |   ...

The column names are given as field IDs, and you would need to browse https://biobank.ndph.ox.ac.uk/showcase/search.cgi to get their meanings. For example, `31-0.0` is sex, `34-0.0` is year of birth, and `54-0.0` is assessment center. On top of this, if a field is categorical then its categories are coded, e.g. in sex `0` means female and `1` means male, and in assessment center `11010` is Leeds and `11009` is New Castle. Finally, you may have hundreds or thousands of these columns. The next step towards having ready-to-use data is to filter out some columns and parse the field IDs and categorical codes. This can be done manually, but automated tools in this repo aim to make it quicker and easier. 



## 4. Extracting Hospital Episode Statistics on particular diseases
If you have a `hesin_all.csv` file which contains all HES data, you can add columns about particular diseases to `12345.csv` using `addnewHES.py`. 

You will need: 
 - `icdGroups.json`: this is a JSON file containing descriptions of required HES codes (as in the examples in this folder). 
 - An existing dataset `input.csv`. 
 - If you want to define prevalent and incident disease, `input.csv` should also contain a date column which will be used to define this. 

Then run: 
```
python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column 'name_of_date_column'
```
This will add a column containing the date of first instance of the given disease definition, as well as a binary column indicating incident disease and a binary column indicating prevalence disease (relative to the date in the specified date column). 
*Note* This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields (40001 and 4002)[https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093]) . 
 
## 5. Advanced usage

### For R fanatics
If you prefer to use R for data preparation, UK Biobank has a built-in tool to facilitate this. However, note this tool doesn't have the column-renaming functionality implemented in prepare_participant_data.  

```Bash 
  # Extracting to R 
  $ ../helpers/linux_tools/ukb_conv /well/doherty/projects/UKBB/participant-data/ukb12345.enc_ukb r -ianalysisCols.txt
  # output = /well/doherty/projects/UKBB/participant-data/ukb12345.r
  # output = /well/doherty/projects/UKBB/participant-data/ukb12345.tab
   
```
The output .r file can be opened and run in R, which will automatically load and relabel categorical columns as needed.  
## To add new codes to an existing dataset: 


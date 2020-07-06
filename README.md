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
Navigate to the repo: 
  ```Bash
  $ cd ukb_download_and_prep_template
  ```

## 2. Extracting participant data to `.csv` format from `.enc_ukb` format
To access specific variables, we extract them from the file which contains all variables in the application for all participants. To do so,  download 12345.enc_ukb file. This can be found on rescomp under: /well/doherty/projects/UKBB/participant-data. 

- First, find the [UK Biobank Data Field IDs](http://biobank.ctsu.ox.ac.uk/crystal/search.cgi) of interest (e.g. [smoking status is 20116](http://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=20116)).
- Append this entry to the file analysisCols.txt
- Extract data to csv format. 

  ```Bash
  # CSV
  $ helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb csv -ianalysisCols.txt
  # output = path_to_data/ukb12345.csv
  
  ```
Note these steps can be done in Windows, Linux or MacOS, but the helper files you need will be slightly different (the tools are in helpers/linux_tools for Linux/MacOS and helpers/windows_tools for Windows). 

How long this extraction will take depends on the number of columns you are extracting, but it is not unusual for it to take several hours. If you just want to add a couple of columns, it is quicker to list them in a separate file (e.g. 'analysisColsMini.txt'), extract a small csv file and merge with the existing file on participant IDs. 

[UK Biobank's guide to accessing the data](https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf) is helpful for any queries. 
## 3. Relabelling and recoding a participant data `.csv` file using Python
## 4. Extracting Hospital Episode Statistics on particular diseases
## 5. Advanced usage



To further prepare this data, go to the folder prepare_participant_data (this folder is Python-based; see note below for R fanatics!).

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

To add new codes to an existing dataset, /well/doherty/projects/UKBB/HES/hesin_all.csv contains all HES data, and the script addnewHES.py can be used. If icdGroups.json is a JSON file containing descriptions of required HES codes (as in the examples in this folder), the usage is as follows: 
```
python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json
 ```
 
*Note* This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields (40001 and 4002)[https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093]) . 
 
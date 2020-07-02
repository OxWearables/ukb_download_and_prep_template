# Downloading UK Biobank participant data

Generally, we will be able to work with the existing copy of the data and simply extract new variables from this ('Working with the existing copy of the data'). Sometimes it will be necessary to download a new copy ('Downloading a new copy of the data') e.g. to work with a different application, or if new variables are released. 

## Working with the existing copy of the data
ukb_copy_41733_application59070.html lists all the variables which are available as part of [Aiden's 59070 application](https://www.ukbiobank.ac.uk/2020/04/statistical-machine-learning-of-wearable-sensor-data-to-predict-disease-outcomes/). 

To access specific variables, we extract them from the file which contains all variables for all participants. To do so,  download 41733.enc_ukb file. This can be found on rescomp under: /well/doherty/projects/UKBB/participant-data. 

- First, find the [UK Biobank Data Field IDs](http://biobank.ctsu.ox.ac.uk/crystal/search.cgi) of interest (e.g. [smoking status is 20116](http://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=20116)).
- Append this entry to the file analysisCols.txt
- Extract data to csv format. 

  ```Bash
  # CSV
  $ ../helpers/linux_tools/ukb_conv /well/doherty/projects/UKBB/participant-data/ukb41733.enc_ukb csv -ianalysisCols.txt
  # output = /well/doherty/projects/UKBB/participant-data/ukb41733.csv
  
  ```
Note these steps can be done in Windows, Linux or MacOS, but the helper files you need will be slightly different (the tools are in helpers/linux_tools for Linux/MacOS and helpers/windows_tools for Windows). 
How long this extraction will take depends on the number of columns you are extracting, but it is not unusual for it to take several hours. If you just want to add a couple of columns, it is quicker to list them in a separate file (e.g. 'analysisColsMini.txt'), extract a small csv file and merge with the existing file on participant IDs. 

[UK Biobank's guide to accessing the data](https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf) is helpful for any queries. 

To further prepare this data, go to the folder prepare_participant_data (this folder is Python-based; see note below for R fanatics!).

### For R fanatics
If you prefer to use R for data preparation, UK Biobank has a built-in tool to facilitate this. However, note this tool doesn't have the column-renaming functionality implemented in prepare_participant_data.  

```Bash 
  # Extracting to R 
  $ ../helpers/linux_tools/ukb_conv /well/doherty/projects/UKBB/participant-data/ukb41733.enc_ukb r -ianalysisCols.txt
  # output = /well/doherty/projects/UKBB/participant-data/ukb41733.r
  # output = /well/doherty/projects/UKBB/participant-data/ukb41733.tab
   
```
The output .r file can be opened and run in R, which will automatically load and relabel categorical columns as needed.  


## Downloading a new copy of the data

This [well documented site on how to access UK Biobank data](http://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=AccessingData) is a good starting point. 
You should carefully read the ['Using UK Biobank data'](http://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=accessing_data_guide#intro) guide to setup decryption keys. 
Therefore, for Aiden's UKB 59070 research application and copy number 41733 we would decrypt to an 'unpacked' file
  ```Bash
  $ ../helpers/linux_tools/ukb_unpack /well/doherty/projects/UKBB/participant_info/ukb41733.enc k59070r41733.key
  # output = /well/doherty/projects/UKBB/participant-data/ukb.enc_ukb
  ```
Note that the rest of this folder assumes you're working with application 59070, copy 41733, so small adjustments will need to be made if you've downloaded a new copy of the data. 

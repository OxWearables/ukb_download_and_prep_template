# Extracting participant data to `.csv` format from `.enc_ukb` format
To access a particular set of variables in `.csv` format, we extract them from the `12345.enc_ukb` file (which contains all variables in the application). 

### Steps
1. Find the [UK Biobank Data Field IDs](http://biobank.ctsu.ox.ac.uk/crystal/search.cgi) of interest (e.g. [smoking status is 20116](http://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=20116)).
2. If it is not already there, append this field to the file `analysisCols.txt`
3. Extract data to `.csv` format:  
  ```Bash
  $ helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb csv -ianalysisCols.txt
  # output = path_to_data/ukb12345.csv
  ```
### Notes 
 - These steps can be done in Windows, Linux or MacOS, but the helper files you need will be slightly different (the tools are in `helpers/linux_tools` for Linux/MacOS and `helpers/windows_tools` for Windows).
 - This may fail initially because `analysisCols.txt` contains a field ID which is not present in the copy of the dataset you are working with. These field IDs should be removed from `analysisCols.txt`. 
 - How long this extraction will take depends on the number of columns you are extracting, but it is not unusual for it to take several hours. If you just want to add a couple of columns, it is quicker to list them in a separate file (e.g. `analysisColsMini.txt`), extract a small `.csv` file and merge with the existing file on participant IDs.
 - Up to this point we are using only standard UK Biobank functionality, so [UK Biobank's guide to accessing the data](https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf) may be helpful.  


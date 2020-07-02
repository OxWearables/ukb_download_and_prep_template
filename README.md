# ukb_download_and_prep_template
This repository provides a template for downloading and preparing [UK Biobank](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi) data.

To access files which have already been downloaded and cleaned, go to the rescomp folder: `/well/doherty/projects/UKBB/`. 

To redownload or process aspects of the data:  
* `download_participant_data` contains details on downloading participant information, principally that collected during UK Biobank assessment centres (or online questionnaires). 
* `prep_participant_data` contains details on preparing downloaded information, including renaming columns and recoding variables according to the data dictionary. 
* `download_accelerometer_data` contains details on downloading accelerometer data. This is a bulk dataset and requires particular care to download. It is very rarely necessary to do this fresh: it is more normal to reprocess the files already stored on the rescomp system. 
* `download_health_data` contains details on downloading Health Episode Statistics data. 
* `helpers` contains utility scripts which are called in processing. 

**Note on applications and copies:** A UK Biobank dataset is associated with a numbered application and, within that application, a numbered copy (this is so subsequent additions of variables to the same application can be distinguished). It is important that the application number is consistent throughout the data downloading and preparation - different applications have a different set of participant IDs, making it impossible to combine them (unless linkage is specifically arranged with UK Biobank). We work or collaborate on several different numbered applications, but, for simplicity and consistency, this download folder assumes you are working with [Aiden's 59070 application](https://www.ukbiobank.ac.uk/2020/04/statistical-machine-learning-of-wearable-sensor-data-to-predict-disease-outcomes). The main copy associated with this application has the number 41733.  

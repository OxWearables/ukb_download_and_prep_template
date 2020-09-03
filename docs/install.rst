# Installation 

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
  
This usage tutorial also assumes you have downloaded and extracted a `.enc_ukb` file (participant data) and a `hesin_all.csv` file (health record data) from UK Biobank. The [download](https://github.com/activityMonitoring/ukb_download_and_prep_template/download) folder contains guidance on how to download these. 

**Note on applications and copies:** A UK Biobank dataset is associated with a numbered application and, within that application, a numbered copy (this is so subsequent additions of variables to the same application can be distinguished). Different applications have access to different sets of variables. Copies from the same application can be merged, but different applications have different participant IDs, so cannot be merged. Throughout this folder we assume we are using copy number 12345 from application 6789.  


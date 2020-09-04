#####################
Getting started
#####################

********************
Why use this tool? 
********************
This tool facilitates analyses using UK Biobank data by automating lots of the data preparation steps. 

*************
Installation
*************

To use this repo, run: 

.. code-block:: sh

   git clone git@github.com:activityMonitoring/ukb_download_and_prep_template
   
This repo requires :code:`pandas` and :code:`nltk`. If you are using an Anaconda installation of Python, these are included. Otherwise, run: 

.. code-block:: sh

   pip install pandas
   pip install nltk
  

Navigate to the repo: 

.. code-block:: sh

  cd ukb_download_and_prep_template
   

*************************
Requirements
*************************
This usage tutorial assumes you have downloaded and extracted a :code:`ukb12345.csv` file containing participant data and a :code:`hesin_all.csv` file containing health record data. `This section <https://ukb-download-and-prep-template.readthedocs.io/en/latest/download.html>`_ contains guidance on how to download these. 

**Note on applications and copies:** A UK Biobank dataset is associated with a numbered application and, within that application, a numbered copy (this is so subsequent additions of variables to the same application can be distinguished). Different applications have access to different sets of variables. Copies from the same application can be merged, but different applications have different participant IDs, so cannot be merged. Throughout this folder we assume we are using copy number 12345 from application 6789.  


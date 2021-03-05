################
Downloading data
################

*****************************
Downloading participant data
*****************************

Here we are using only standard UK Biobank functionality, so `UK Biobank's guide to accessing the data <https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.3.pdf>`_ is a very useful reference. 

You will have initially downloaded an encrypted :code:`ukb12345.enc` file. This needs to be decrypted using the key provided by UK Biobank in an email e.g. for research application 6789 and copy number 12345 we would decrypt to an 'unpacked' file: 

  .. code-block:: sh

     download/helpers/linux_tools/ukb_unpack path_to_data/ukb12345.enc k6789r12345.key
     download/helpers/linux_tools/ukb_unpack path_to_data/ukb12345.enc k6789r12345.key
     # output = path_to_data/ukb12345.enc_ukb
     
     
    
To extract data from this to :code:`.csv` format, see the `next section <https://ukb-download-and-prep-template.readthedocs.io/en/latest/extract.html>`_. 

*********************************************************************************
Extracting participant data to :code:`.csv`
*********************************************************************************

To access a particular set of variables in :code:`.csv` format, we extract them from the :code:`12345.enc_ukb` file (which contains all variables in the application). 

======
Steps
======
1. Find the `UK Biobank Data Field IDs <http://biobank.ctsu.ox.ac.uk/crystal/search.cgi>`_ of interest (e.g. `smoking status is 20116 <http://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=20116>`_).
2. If it is not already there, append this field to the file :code:`analysisCols.txt`
3. Extract data to :code:`.csv` format:

  .. code-block:: sh

     download/helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb csv -ianalysisCols.txt
     # output = path_to_data/ukb12345.csv
  
  
======
Notes 
======
- These steps can be done in Windows, Linux or MacOS, but the helper files you need will be slightly different (the tools are in :code:`download/helpers/linux_tools` for Linux/MacOS and :code:`download/helpers/windows_tools` for Windows).
- This may fail initially because :code:`analysisCols.txt` contains a field ID which is not present in the copy of the dataset you are working with. These field IDs should be removed from :code:`analysisCols.txt`. 
- How long this extraction will take depends on the number of columns you are extracting, but it is not unusual for it to take several hours. If you just want to add a couple of columns, it is quicker to list them in a separate file (e.g. :code:`analysisColsMini.txt`), extract a small :code:`.csv` file and merge with the existing file on participant IDs.



************************
Downloading health data
************************

UK Biobank benefits from passive follow-up via health record linkage.

To understand the available datasets: 
- Here is `a good summary of what health outcomes data exists and pros and cons of using different aspects <http://biobank.ndph.ox.ac.uk/showcase/showcase/docs/HealthOutcomesOverview.pdf>`_ (up-to-date as of Sep 2019).
- Note the `dates for which HES data are available <https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=Data_providers_and_dates>`_.

Here, we discuss Hospital Episode Statistics: `ICD9/10 codes <https://www.who.int/classifications/icd/icdonlineversions/en/>`_ from hospital admissions. If you require Operations and Procedures codes or primary care codes, these need to be processed separately. 

==============
Steps
==============
1. Follow the `UKB guide to access the data portal <http://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf>`_. 
2. It is easiest to download the whole table for the relevant data type (e.g. hesin is required for using all the others, hesin_diag provides diagnosis codes, hesin_oper operation codes).
	- You can do this by putting the name of the data table in the box provided in the Table Download tab. 

	- If you wish to use the data portal, these SQL statements will download all diagnosis codes from :code:`hesin_diag` and hospital episode information from :code:`hesin:`
	
	.. code-block:: sql
	  
	        SELECT eid, ins_index, admidate, disdate, epiend, epistart FROM hesin * then click 'Download'
		SELECT * FROM hesin_diag * click 'Download'
	  
  
3. Join files together in preparation for future use. 

	  .. code-block:: sh
	  
		# Rename files if necessary to match the names used here
		# Call python script to merge files together and delete downloaded input files
		python mergeHESfiles.py ~/Downloads/ukb.txt ~/Downloads/ukb_diag.txt \
		~/Downloads/hesin_all.csv




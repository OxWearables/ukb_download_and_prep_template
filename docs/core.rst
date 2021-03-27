##################
Basic usage
##################

**************************************************************
Relabelling and recoding participant data
**************************************************************
You should have an extracted :code:`ukb12345.csv` file (extracted from :code:`.enc_ukb` file) to work with (if not, see `this section <https://ukb-download-and-prep-template.readthedocs.io/en/latest/download.html>`_). It should look something like this:

+---------+--------+--------+--------+--------+
| eid     | 31-0.0 | 34-0.0 | 54-0.0 |   ...  | 
+=========+========+========+========+========+
| 4987419 | 0      | 1944   | 11016  |   ...  |
+---------+--------+--------+--------+--------+
| 2898413 | 0      | 1956   | 11009  |   ...  |
+---------+--------+--------+--------+--------+
| 1049655 | 1      | 1947   | 11010  |   ...  |
+---------+--------+--------+--------+--------+
| 1892589 | 1      | 1941   | 11011  |   ...  |
+---------+--------+--------+--------+--------+
| 2449164 | 1      | 1958   | 11010  |   ...  |
+---------+--------+--------+--------+--------+

(This is fake data - Any resemblance to real UK Biobank participants is coincidental!)

- The column names are given as field IDs, and you would need to browse `<https://biobank.ndph.ox.ac.uk/showcase/search.cgi>`_ to get their meanings. For example, :code:`31-0.0` is sex, :code:`34-0.0` is year of birth, and :code:`54-0.0` is assessment center. 
- If a field is categorical then its categories are coded e.g. in sex :code:`0` means female and :code:`1` means male, and in assessment center :code:`11010` is Leeds and :code:`11009` is Newcastle. 
- You may have hundreds or thousands of these columns. 

Therefore, the next step towards having ready-to-use data is to filter out some columns and parse the field IDs and categorical codes. (While this can be done manually, the automated tools in this repo aim to make it quicker and easier.)

======
Steps
======
1. Auto-generate a :code:`columns.json` file from the text file of field IDs (in the format used in :code:`download_participant_data`):

	.. code-block:: sh
  
	   python writeColumnsFile.py --columnsFile analysisCols.txt 


2. Run:

	.. code-block:: sh
  
       	   python filterUKB.py ukb12345.csv -o outputFilename.csv

If you want to customise the behaviour or add subsequent columns manually, see `the Advanced Usage options <https://ukb-download-and-prep-template.readthedocs.io/en/latest/advanced.html>`_


*********************************************************
Adding Hospital Episode Statistics
*********************************************************

In this section we will add columns on disease diagnoses in hospital to an existing participant dataset (:code:`input.csv`). 
You will need:

- :code:`hesin_all.csv`: a file containing Hospital Episode Statistics data for all participants (see `here <https://ukb-download-and-prep-template.readthedocs.io/en/latest/health.html>`_).
- :code:`icdGroups.json`: a JSON file describing required HES codes (here's an `example <https://github.com/activityMonitoring/ukb_download_and_prep_template/blob/master/icdGroups.json>`_). 
- An existing dataset :code:`input.csv` (such as :code:`outputFilename.csv` from the last section). 
- If you want to define prevalent and incident disease, :code:`input.csv` should also contain a date column which will be used to define this. 

Then run:

.. code-block:: sh

   python addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column name_of_date_column

This will add a column containing the date of first instance of the given disease definition, as well as a binary column indicating incident disease and a binary column indicating prevalent disease (relative to the date in the specified date column). 

=========
Notes
=========

- The JSON file should have :code:`level` specified. :code:`"level": "primary"` identifies only diagnoses which were the primary diagnosis in the admission, whereas :code:`"level": "all"` identifies all diagnoses.
- This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields `40001 and 40002 <https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093>`_ or `via the Data Portal <https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=COVID19_availability>`_) .
- Please note that if you used or are using a version of this repo from before 19.02.2021, an error in date processing may have caused wrongly assigned dates for health outcomes. Please re-download and re-process any data processed with `addNewHES.py`.




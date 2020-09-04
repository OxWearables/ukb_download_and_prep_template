=========================================================
Adding Hospital Episode Statistics on particular diseases
=========================================================
In this section we will add columns on disease diagnoses in hospital to an existing participant dataset (:code:`input.csv`). 

You will need: 
 - :code:`hesin_all.csv`: this is a file containing Hospital Episode Statistics data for all participants. 
 - :code:`icdGroups.json`: this is a JSON file containing descriptions of required HES codes (as in the examples in this folder). 
 - An existing dataset :code:`input.csv` (which might be :code:`outputFilename.csv` from the last section). 
 - If you want to define prevalent and incident disease, :code:`input.csv` should also contain a date column which will be used to define this. 

Then run:

.. code-block:: console

   python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column 'name_of_date_column'

This will add a column containing the date of first instance of the given disease definition, as well as a binary column indicating incident disease and a binary column indicating prevalent disease (relative to the date in the specified date column). 
Note the JSON file should have :code:`level` specified. :code:`"level": "primary"` identifies only diagnoses which were the primary diagnosis in the admission, whereas :code:`"level": "all"` identifies all diagnoses.

**Note:** This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields `40001 and 4002 <https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093>`_) . 


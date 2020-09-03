=========================================================
Adding Hospital Episode Statistics on particular diseases
=========================================================
In this section we will add columns on disease diagnoses in hospital to an existing participant dataset (`input.csv`). 

You will need: 
 - `hesin_all.csv`: this is a file containing Hospital Episode Statistics data for all participants. 
 - `icdGroups.json`: this is a JSON file containing descriptions of required HES codes (as in the examples in this folder). 
 - An existing dataset `input.csv` (which might be `outputFilename.csv` from the last section). 
 - If you want to define prevalent and incident disease, `input.csv` should also contain a date column which will be used to define this. 

Then run: 
.. code-block::
        python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column 'name_of_date_column

This will add a column containing the date of first instance of the given disease definition, as well as a binary column indicating incident disease and a binary column indicating prevalent disease (relative to the date in the specified date column). 
Note the JSON file should have `level` specified. `"level": "primary"` identifies only diagnoses which were the primary diagnosis in the admission, whereas `"level": "all"` identifies all diagnoses. 
**Note:** This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields `40001 and 4002 <https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093>`) . 


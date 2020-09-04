#########################################################
Adding Hospital Episode Statistics
#########################################################

In this section we will add columns on disease diagnoses in hospital to an existing participant dataset (:code:`input.csv`). 
You will need:

- :code:`hesin_all.csv`: a file containing Hospital Episode Statistics data for all participants (see `here <https://ukb-download-and-prep-template.readthedocs.io/en/latest/health.html>`_).
- :code:`icdGroups.json`: a JSON file describing required HES codes (here's an `example <https://github.com/activityMonitoring/ukb_download_and_prep_template/blob/master/icdGroups.json>`_). 
- An existing dataset :code:`input.csv` (such as :code:`outputFilename.csv` from the last section). 
- If you want to define prevalent and incident disease, :code:`input.csv` should also contain a date column which will be used to define this. 

Then run:

.. code-block:: sh

   python addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column 'name_of_date_column'

This will add a column containing the date of first instance of the given disease definition, as well as a binary column indicating incident disease and a binary column indicating prevalent disease (relative to the date in the specified date column). 

=========
Notes
=========

- The JSON file should have :code:`level` specified. :code:`"level": "primary"` identifies only diagnoses which were the primary diagnosis in the admission, whereas :code:`"level": "all"` identifies all diagnoses.
- This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields `40001 and 40002 <https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093>`_ or `via the Data Portal <https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=COVID19_availability>`_) . 


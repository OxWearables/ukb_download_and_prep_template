##############################################################
Relabelling and recoding participant data
##############################################################
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

If you want to customise the behaviour or add subsequent columns manually, see the advanced usage options.

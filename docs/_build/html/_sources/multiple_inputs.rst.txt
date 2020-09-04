################################################
Working with multiple :code:`ukbXXXX.csv` files
################################################
Sometimes we have multiple UKB files because we requested more variables later during the project and these extra variables come separately. In that case, the tool can take multiple UKB files:

.. code-block:: console

   python filterUKB.py ukb12345.csv ukb54321.csv -o outputFilename.csv


========================================
Working with multiple `ukbXXX.csv` files
========================================
Sometimes we have multiple UKB files because we requested more variables later during the project and these extra variables come separately. In that case, the tool can take multiple UKB files:
.. code-block::
        python filterUKB.py ukb12345.csv ukb54321.csv -o outputFilename.csv

============================
Including field ID suffixes
=============================
When automatically parsing the field ID, by default it will drop the suffixes `-X.Y` (indicating visit number and array index, for example `-0.0`, `-1.0`, etc). If you need to keep these, set the key `drop_suffix=False` and it will append the suffixes as `_X_Y`. For example,

.. code-block:: 
        {
            # ...

            "1558-0.0":{
                "drop_suffix": False,
            },

            # ...
        }

will produce the column name `AlcoholIntakFrequenc_0_0`.

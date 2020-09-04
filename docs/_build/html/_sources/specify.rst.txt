#############################################
Specifying particular relabelling or recoding 
#############################################
The tool automatically renames columns and recodes categorical variables.  This is using UK Biobank's Data Dictionary and coding schema (:code:`Data_Dictionary_Showcase.csv` and :code:`Codings_Showcase.csv`; available from UK Biobank's website). 

For the column name parsing, it uses UKB's field description, which works reasonably well unless the description is very long. For example, :code:`6153` (medication for cholesterol, blood pressure, diabetes, or take exogenous hormones) gets the mouthful :code:`MedCholesterolBloodPressDiabetTakExogHormon`

It is possible to customize the column name by specifying a :code:`name` key. It is also possible to customize the categorical values (e.g. if you want to recategorize) by specifying a :code:`replace_values` key. In the last example, further editing :code:`columns.json` to say: 

.. code-block:: json

        {
            # ...

            "1558-0.0":{
                'name': 'Booze',
                'replace_values': {
                    1: "weekly",  # Daily or almost daily
                    2: "weekly",  # 3-4 times a week
                    3: "weekly",  # 1-2 times a week
                    4: "rarely",  # 1-3 times a month
                    5: "rarely",  # Special occasions only
                    6: "never",   # Never
                   -3: np.nan,    # Prefer not to answer
                }
            },

            # ...
        }

and running :code:`filterUKB.py` as above will convert the previous column to

+----------------------------+
| Booze                      |
+============================+
| weekly                     |
+----------------------------+
| rarely                     |
+----------------------------+
| rarely                     |
+----------------------------+
| rarely                     |
+----------------------------+
| weekly                     |
+----------------------------+
| never                      |
+----------------------------+
| ...                        |
+----------------------------+

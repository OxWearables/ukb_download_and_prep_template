======================
Adding derived columns
======================

You might have to create new columns based on operations on other columns. To use this option, :code:`filterUKB.py` must be run with the optional argument :code:`--derived_columns True`. 

The :code:`derivedColumns.json` file is used to specify the operations used to create columns. The file included in this folder contains some common options to derive. 

For example, there are (confusingly) three columns corresponding to date of death: :code:`40001-0.0`, :code:`40001-1.0` and :code:`40001-2.0`. It makes sense that the earliest of these is the date of death. To do this, open :code:`derivedColumns.json` and add:

.. code-block:: json 

   { 
   # ...
      'DateOfDeath': {
            'columns': ['40000-0.0', '40000-1.0', '40000-2.0'],
            'func': lambda df: df.astype('datetime64').min(axis=1),
        } #,
   # ...
   }

The :code:`columns` key defines which columns of the raw UKB table to select, and :code:`func` defines the function to operate on the resulting subtable. Alternatively, you can also omit :code:`columns` and write :code:`func` directly as :code:`lambda df: df[['40000-0.0', '40000-1.0', '40000-2.0']].astype('datetime64').min(axis=1)`. Your output CSV will now have a column that looks like this:

+----------------------------+
| DateOfDeath                |
+============================+
| 2013-08-17                 |
+----------------------------+
| NaN                        |
+----------------------------+
| NaN                        |
+----------------------------+
| 2015-03-07                 |
+----------------------------+
| NaN                        |
+----------------------------+
| ...                        |
+----------------------------+

See :code:`derivedColumns.json` for more examples.

======================
Adding derived columns
======================

You might have to create new columns based on operations on other columns. To use this option, `filterUKB.py` must be run with the optional argument `--derived_columns True`. 

The `derivedColumns.json` file is used to specify the operations used to create columns. The file included in this folder contains some common options to derive. 

For example, there are (confusingly) three columns corresponding to date of death: `40001-0.0`, `40001-1.0` and `40001-2.0`. It makes sense that the earliest of these is the date of death. To do this, open `derivedColumns.json` and add:


.. code-block:: 
        # ...

        'DateOfDeath': {
            'columns': ['40000-0.0', '40000-1.0', '40000-2.0'],
            'func': lambda df: df.astype('datetime64').min(axis=1),
        },

        # ...
    }

The `columns` key defines which columns of the raw UKB table to select, and `func` defines the function to operate on the resulting subtable. Alternatively, you can also ommit `columns` and write `func` directly as `lambda df: df[['40000-0.0', '40000-1.0', '40000-2.0']].astype('datetime64').min(axis=1)`. Your output CSV will now have a column that looks like this:
+----------------------------+
| DateOfDeath                |
+----------------------------+
| 2013-09-15                 |
| NaN                        |
| NaN                        |
| 2015-02-01                 |
| NaN                        |
| ...                        |
+----------------------------+

See `derivedColumns.json` for more examples.

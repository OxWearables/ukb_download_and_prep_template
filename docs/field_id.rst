===========================
Including field ID suffixes
===========================

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

###########################
Including field ID suffixes
###########################

When automatically parsing the field ID, by default it will drop the suffixes :code:`-X.Y` (indicating visit number and array index, for example :code:`-0.0`, :code:`-1.0`, etc). If you need to keep these, set the key :code:`drop_suffix=False` and it will append the suffixes as :code:`_X_Y`. For example,

.. code-block:: json

   {
    # ...
    "1558-0.0":{
        "drop_suffix": False,
        },
    # ...
    }

will produce the column name :code:`AlcoholIntakFrequenc_0_0`.

# Prepare participant data

This folder contains tools to help prepare downloaded participant data, including filtering and parsing field IDs and categorical codes of UKB files. 

*Requires:* `pandas`, `nltk` &mdash; these are included in Anaconda.

## Why this tool?

After you downloaded and converted your UKB file to CSV format as per the user guide, you get a cryptic `ukb12345.csv` that looks something like this:

| eid     | 31-0.0 | 34-0.0 | 52-0.0 | 53-0.0     | 54-0.0 |   ...
|---------|--------|--------|--------|------------|--------|--------
| 4937419 | 1      | 1944   | 8      | 2009-01-12 | 11010  |   ...
| 2860412 | 0      | 1951   | 7      | 2008-12-11 | 11009  |   ...
| 1039354 | 0      | 1945   | 12     | 2008-07-28 | 11010  |   ...
| 1592599 | 1      | 1939   | 3      | 2009-02-09 | 11011  |   ...
| 3849156 | 1      | 1958   | 1      | 2009-02-27 | 11016  |   ...

The column names are given as field IDs, and you would need to browse https://biobank.ndph.ox.ac.uk/showcase/search.cgi to get their meanings. For example, `31-0.0` is sex, `34-0.0` is year of birth, and `54-0.0` is assessment center. On top of this, if a field is categorical then their categories are coded, e.g. in sex `0` means female and `1` means male, and in assessment center `11010` is Leeds and `11009` is Newcastle. Finally, you may have hundreds or thousands of these columns. Your next step is probably to filter out some columns and parse through the field IDs and categorical codes. This tool attempts to make this processes a little bit easier.

## Usage

### Basic data preparation
1. Auto-generate a `columns.py` file from the text file of field IDs (in the format used in download_participant_data):
 ```
 python write_columns_file.py --columns_text_file analysisCols.txt
 ``` 
 This automatically generates a file listing the first measurement at the first assessment of the given variable. Alternatively, and if you want to customise the behaviour or add other columns (or repeat measurements), you can add desired field IDs in `columns.py` following the format described below. 
 2. Run:

```
python filter_ukb.py ukb12345.csv -o output_filename.csv
```
`output_filename.csv` has columns named according to the variable name, and Note the default behaviour is to use the first measurement from the first assessment visit: this generally works well, but has some problems (e.g. certain columns like blood pressure had multiple measurements taken as standard, whcih you may wish to use). 

### Manually adding a field ID to `columns.py`
Sometimes, you may wish to manually add certain fields. For example, to add the second measurement of systolic blood pressure (field 93), open `columns.py` and under the `COLUMNS` dictionary add:
```python
COLUMNS = {
    # ...

    "93-0.1":{},

    # ...
}
```
To add `1558` (alcohol intake frequency), open `columns.py` and under the `COLUMNS` dictionary add:

```python
COLUMNS = {
    # ...

    "1558-0.0":{},

    # ...
}
```

Then after running `python filter_ukb.py...` your output CSV will have a column that looks like this:

| AlcoholIntakFrequenc       |
|----------------------------|
| Three or four times a week |
| Special occasions only     |
| One to three times a month |
| One to three times a month |
| Daily or almost daily      |
| Never                      |
| ...                        |

The field ID and categorical codes have been automatically translated. This is done by looking at `Data_Dictionary_Showcase.csv` and `Codings_Showcase.csv`, files that can be downloaded from the UKB's website. Particularly for the column name parsing, it uses UKB's field description, which works reasonably well unless the description is very long. For example, `6153` (medication for cholesterol, blood pressure, diabetes, or take exogenous hormones) gets the mouthful `MedCholesterolBloodPressDiabetTakExogHormon`

It is possible to customize the column name by specifying a `name` key. It is also possible to customize the categorical values (e.g. if you want to recategorize) by specifying a `replace_values` key. In the last example,

```python
COLUMNS = {
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
```
will convert the previous column to

| Booze                      |
|----------------------------|
| weekly                     |
| rarely                     |
| rarely                     |
| rarely                     |
| weekly                     |
| never                      |
| ...                        |

See `columns.py` for more examples.

## Derived columns
Another processing pattern that you might have is to create new columns based on operations on other columns. To use this option, `filter_ukb.py` must be run with the optional argument `--derived_columns True`, and the columns used for the derivation must be added to `columns.py` (if they are not already there). 

The `derived_columns.py` file is used to specify the operations used to create columns. The file included contains some common options to derive (but note the required columns must be added to `columns.py`). 

For example, there are (confusingly) three columns corresponding to date of death: `40001-0.0`, `40001-1.0` and `40001-2.0`. It makes sense that the earliest of these is the date of death. To do this, open `derived_columns.py` and under the `DERIVED_COLUMNS` dictionary add:

```python
    DERIVED_COLUMNS: {
        # ...

        'DateOfDeath': {
            'columns': ['40000-0.0', '40000-1.0', '40000-2.0'],
            'func': lambda df: df.astype('datetime64').min(axis=1),
        },

        # ...
    }
```
The `columns` key defines which columns of the raw UKB table to select, and `func` defines the function to operate on the resulting subtable. Alternatively, you can also ommit `columns` and write `func` directly as `lambda df: df[['40000-0.0', '40000-1.0', '40000-2.0']].astype('datetime64').min(axis=1)`. Your output CSV will now have a column that looks like this:

| DateOfDeath                |
|----------------------------|
| 2013-09-15                 |
| NaN                        |
| NaN                        |
| 2015-02-01                 |
| NaN                        |
| ...                        |

See `derived_columns.py` for more examples.

## Miscellaneous

### Multiple `ukbXXX.csv` files
Sometimes we have multiple UKB files because we requested more variables later during the project and these extra variables come separately. In that case, the tool can take multiple UKB files:

`python filter_ukb.py ukb12345.csv ukb67890.csv -o output_filename.csv`

### Field ID suffixes
When automatically parsing the field ID, by default it will drop the suffixes `-X.Y` (indicating visit number and array index, for example `-0.0`, `-1.0`, etc). If you need to keep these, set the key `drop_suffix=False` and it will append the suffixes as `_X_Y`. For example,

```python
COLUMNS = {
    # ...

    "1558-0.0":{
        "drop_suffix": False,
    },

    # ...
}
```
will produce the column name `AlcoholIntakFrequenc_0_0`.

### Disable parsing
If for some reason you don't want to automatically parse the field ID and/or the categorical codes, you can explicitly set the keys `name` and/or `replace_values` to `None`. For example,

```python
COLUMNS = {
    # ...

    "1558-0.0":{
        "name": None,
        "replace_values": None,
    },

    # ...
}
```
will leave the column untouched:
| 1558-0.0 |
|----------|
| 2        |
| 5        |
| 4        |
| 4        |
| 1        |
| 6        |
| ...      |

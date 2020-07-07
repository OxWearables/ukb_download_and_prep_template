# ukb_download_and_prep_template

This repository aims to provide a template for the preparation of [UK Biobank](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi) participant and health record data. It is split into sections on: 
 1. Installation 
 2. Extracting participant data to `.csv` format from `.enc_ukb` format
 3. Relabelling and recoding a participant data `.csv` file using Python
 4. Extracting Hospital Episode Statistics on particular diseases
 5. Advanced usage

This folder assumes you have downloaded and extracted a `.enc_ukb` file (participant data) and a `hesin_all.csv` file (health record data) from UK Biobank. The [download](https://github.com/activityMonitoring/ukb_download_and_prep_template/download) folder contains guidance on how to download these. 

A UK Biobank dataset is associated with a numbered application and, within that application, a numbered copy (this is so subsequent additions of variables to the same application can be distinguished). Different applications have access to different sets of variables. Throughout this folder we assume we are using copy number 12345.  

## 1. Installation 

To use this repo, run: 
  ```Bash
  $ git clone git@github.com:activityMonitoring/ukb_download_and_prep_template
  ```
 
This repo requires `pandas` and `nltk`. If you are using an Anaconda installation of Python, these are included. Otherwise, run: 
  ```Bash
  $ pip install pandas
  $ pip install nltk
  ```

Navigate to the repo: 
  ```Bash
  $ cd ukb_download_and_prep_template
  ```

## 2. Extracting participant data to `.csv` format from `.enc_ukb` format
To access a particular set of variables in `.csv` format, we extract them from the `12345.enc_ukb` file (which contains all variables in the application for all participants). 

	1. Find the [UK Biobank Data Field IDs](http://biobank.ctsu.ox.ac.uk/crystal/search.cgi) of interest (e.g. [smoking status is 20116](http://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=20116)).
	2. If it is not already there, append this entry to the file `analysisCols.txt`
	3. Extract data to `.csv` format:  

	  ```Bash
	  # CSV
	  $ helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb csv -ianalysisCols.txt
	  # output = path_to_data/ukb12345.csv
	  
	  ```
### Usage notes 
 - These steps can be done in Windows, Linux or MacOS, but the helper files you need will be slightly different (the tools are in helpers/linux_tools for Linux/MacOS and helpers/windows_tools for Windows).
 - This may fail initially because `analysisCols.txt` contains a field ID which is not present in this copy of the dataset. These field IDs should be removed from `analysisCols.txt`. 
 - How long this extraction will take depends on the number of columns you are extracting, but it is not unusual for it to take several hours. If you just want to add a couple of columns, it is quicker to list them in a separate file (e.g. `analysisColsMini.txt`), extract a small `.csv` file and merge with the existing file on participant IDs. 
 -[UK Biobank's guide to accessing the data](https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.1.pdf) is helpful for queries. 

## 3. Relabelling and recoding a participant data `.csv` file using Python
Your `ukb12345.csv` from the last step looks something like this:

| eid     | 31-0.0 | 34-0.0 | 52-0.0 | 53-0.0     | 54-0.0 |   ...
|---------|--------|--------|--------|------------|--------|--------
| 4937419 | 1      | 1944   | 8      | 2009-01-12 | 11010  |   ...
| 2860412 | 0      | 1951   | 7      | 2008-12-11 | 11009  |   ...
| 1039354 | 0      | 1945   | 12     | 2008-07-28 | 11010  |   ...
| 1592599 | 1      | 1939   | 3      | 2009-02-09 | 11011  |   ...
| 3849156 | 1      | 1958   | 1      | 2009-02-27 | 11016  |   ...

The column names are given as field IDs, and you would need to browse https://biobank.ndph.ox.ac.uk/showcase/search.cgi to get their meanings. For example, `31-0.0` is sex, `34-0.0` is year of birth, and `54-0.0` is assessment center. On top of this, if a field is categorical then its categories are coded, e.g. in sex `0` means female and `1` means male, and in assessment center `11010` is Leeds and `11009` is New Castle. Finally, you may have hundreds or thousands of these columns. The next step towards having ready-to-use data is to filter out some columns and parse the field IDs and categorical codes. This can be done manually, but automated tools in this repo aim to make it quicker and easier. 



## 4. Extracting Hospital Episode Statistics on particular diseases
If you have a `hesin_all.csv` file which contains all HES data, you can add columns about particular diseases to `12345.csv` using `addnewHES.py`. 

You will need: 
 - `icdGroups.json`: this is a JSON file containing descriptions of required HES codes (as in the examples in this folder). 
 - An existing dataset `input.csv`. 
 - If you want to define prevalent and incident disease, `input.csv` should also contain a date column which will be used to define this. 

Then run: 
```
python3 addNewHES.py input.csv hesin_all.csv output.csv icdGroups.json --incident_prevalent True --date_column 'name_of_date_column'
```
This will add a column containing the date of first instance of the given disease definition, as well as a binary column indicating incident disease and a binary column indicating prevalence disease (relative to the date in the specified date column). 
*Note* This dataset includes hospital admissions only. You may also want to extract appearance of these codes on death certificates, which are available in the download of participant data (fields (40001 and 4002)[https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=100093]) . 
 
## 5. Advanced usage
### Adding a field ID to `columns.py` and specifying particular recoding/ renaming
Rather than using the autogenerated file for recoding columns, we can manually update `columns.py` to add columns or to specify particular recoding and renaming behaviour for these columns. 

For example, to add `1558` (alcohol intake frequency), open `columns.py` and under the `COLUMNS` dictionary add:

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
### Derived columns
You might have to create new columns based on operations on other columns. To use this option, `filter_ukb.py` must be run with the optional argument `--derived_columns True`, and the columns used for the derivation must be manually added to `columns.py`. 

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



### For R fanatics
If you prefer to use R for data preparation, UK Biobank has a built-in tool to facilitate this. However, note this tool doesn't have the column-renaming functionality and additional flexibility on recoding implemented as part of this tool.  

```Bash 
  # Extracting to R 
  $ helpers/linux_tools/ukb_conv path_to_data/ukb12345.enc_ukb r -ianalysisCols.txt
  # output = path_to_data/ukb12345.r
  # output = path_to_data/ukb12345.tab
   
```
The output .r file can be opened and run in R, which will automatically load and relabel categorical columns as needed.  

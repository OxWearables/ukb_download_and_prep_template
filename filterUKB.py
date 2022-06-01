"""
Edit columns.json to select the desired UKB columns to include and parse.
Edit derivedColumns.json to define new derived columns.
See https://biobank.ndph.ox.ac.uk/showcase/search.cgi to search for field IDs
"""

import argparse
import pandas as pd
from functools import reduce
import nltk
from nltk.corpus import stopwords
import time
import json
import numpy as np
from tqdm import tqdm

def concat_strings(df, sep="", fillna=np.nan):
    """ Concatenate along each row of strings, e.g.

    'a', 'b', 'c'        'abc'
    'd', 'e', nan,  ->   'de'
    'g', nan, 'i',       'gi'

    """
    result = df[df.columns[0]].str.cat([df[c] for c in df.columns[1:]], sep="__sep__", na_rep="__na__")
    result = result.apply(lambda s: sep.join([w for w in s.split("__sep__") if w != "__na__"]))
    result = result.replace("", fillna)
    return result
    
pd.options.mode.chained_assignment = None


def main(args):

    COLUMNS = json.loads(open(args.columnsFile).read())
    # List of column names with eid for use in read_csv
    COLUMNS_LIST = list(COLUMNS.keys())
    COLUMNS_LIST.extend(['eid'])

    if args.derivedColumns:
        DERIVED_COLUMNS = json.loads(open(args.derivedColumnsFile).read())
        [COLUMNS_LIST.extend(DERIVED_COLUMNS[k]['columns']) for k in DERIVED_COLUMNS.keys()]

    
    # Download a required packages for parsing
    nltk.download('punkt')
    nltk.download('stopwords')

    before = time.time()
    print("Loading UKB file(s)...", flush=True, end=" ")

    dfs = []
    chunksize = 10000
    for in_df in args.ukbfile:
        print("Processing: ", in_df)
        df=pd.DataFrame()
        df_cols = pd.read_csv(in_df, nrows=0).columns.tolist()
        col_list = list(set.intersection(set(df_cols), set(COLUMNS_LIST)))

        chunks = pd.read_csv(in_df,\
                   chunksize=chunksize, low_memory=False, \
                   index_col="eid", usecols=col_list)
        
        tmp_df = pd.concat(chunk for chunk in tqdm(chunks, unit=" rows", unit_scale=chunksize))
        dfs.append(tmp_df)

    df = reduce(lambda left,right: left.join(right, lsuffix="", rsuffix="_duplicate"), dfs)
    print(f"({time.time()-before:.2f}s)")

    column_parser = ColumnParser(args.datafile, args.codefile)

    df_new = df[list(COLUMNS.keys())]

    if args.derivedColumns:
        for col, info in DERIVED_COLUMNS.items():
            print(f'Deriving column {col}...', flush=True, end=" ")
            before = time.time()

            other_cols = info['columns']
            func = eval(info['func'])
            df_new[col] = func(df[other_cols])

            print(f"({time.time()-before:.2f}s)")

    for col, info in COLUMNS.items():
        before = time.time()
        print(f"Parsing column {col} ->", flush=True, end=" ")

        colname = info.get('name', True)
        drop_suffix = info.get('drop_suffix', True)
        if (drop_suffix == "False"): 
            drop_suffix = False

        replace_values = info.get('replace_values', True)

        if replace_values is True:
            replace_values = column_parser.parse_values(col)
        if replace_values is not None:
            #df_new[col] = df_new[col].astype(str)
            df_new[col] = df_new[col].apply(lambda x : str(x).split('.', 1)[0])
            df_new[col] = df_new[col].astype(str).replace(replace_values)

        if colname is True:
            colname = column_parser.parse_colname(col, drop_suffix)
        if colname is not None:
            df_new.rename(columns={col:colname}, inplace=True)

        print(f"{colname} ({time.time()-before:.2f}s)")

    

    print(f"Saving to {args.outfile}...", flush=True, end=" ")
    before = time.time()
    df_new.to_csv(args.outfile)
    print(f"Done! ({time.time()-before:.2f}s)")


class ColumnParser():
    # stemmer = nltk.stem.PorterStemmer()
    stemmer_lancaster = nltk.stem.LancasterStemmer()
    stemmer_snowball = nltk.stem.SnowballStemmer("english")

    def __init__(self, datafile, codefile):
        self.data_df = pd.read_csv(datafile)
        self.code_df = pd.read_csv(codefile)

    def parse_colname(self, col, drop_suffix=True):
        fieldID, suffix1, suffix2 = ColumnParser.parse_col(col)
        field_desc = self.data_df[self.data_df['FieldID']==fieldID]['Field'].values[0]
        colname = self.shorten_description(field_desc)
        if not drop_suffix:
            colname += f'_{suffix1}_{suffix2}'
        return colname

    def parse_values(self, col):
        if not self.is_categorical(col):
            return None
        else:
            fieldID, _, _ = ColumnParser.parse_col(col)
            coding = self.data_df[self.data_df['FieldID']==fieldID]['Coding'].values[0]
            values_and_meanings = self.code_df[self.code_df['Coding']==coding][['Value', 'Meaning']].values
            values, meanings = values_and_meanings[:,0], values_and_meanings[:,1]
            values = values.astype('str')
            replace_values = dict(zip(values, meanings))
            return replace_values

    def is_categorical(self, col):
        fieldID, _, _ = ColumnParser.parse_col(col)
        valuetype = self.data_df[self.data_df['FieldID']==fieldID]['ValueType'].values[0]
        return valuetype in ('Categorical single', 'Categorical multiple')

    @staticmethod
    def shorten_description(desc):
        words = nltk.word_tokenize(desc)
        words = [w for w in words if w not in "?:!.,;--/"]  # remove punctuations
        if len(words) > 3:  # use more aggresive stemming for long desc
            words = [w for w in words if w not in stopwords.words("english")]
            stemmer = ColumnParser.stemmer_lancaster
        else:
            stemmer = ColumnParser.stemmer_snowball
        short_desc = "".join([stemmer.stem(w).capitalize() for w in words])
        return short_desc

    @staticmethod
    def parse_col(col):
        fieldID, suffixes = col.split("-")
        suffix1, suffix2 = suffixes.split(".")
        fieldID, suffix1, suffix2 = int(fieldID), int(suffix1), int(suffix2)
        return fieldID, suffix1, suffix2



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ukbfile', nargs='+')
    parser.add_argument('--datafile', default='Data_Dictionary_Showcase.csv')
    parser.add_argument('--codefile', default='Codings_Showcase.csv')
    parser.add_argument('--outfile', '-o', required=True)
    parser.add_argument('--derivedColumns', default = False)
    parser.add_argument('--derivedColumnsFile', default = "derivedColumns.json")
    parser.add_argument('--columnsFile', default = "columns.json")
    args = parser.parse_args()

    main(args)

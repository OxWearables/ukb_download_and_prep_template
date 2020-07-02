import numpy as np


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


DERIVED_COLUMNS = {
    # ---------------------------------------
    # Usage:
    #
    # 'SumOfXXAndYY': {
    #     'columns': ['XX', 'YY'],
    #     'func': lambda df: df.sum(axis=1),
    # },
    # ---------------------------------------

    'DateOfBirth': {
        'columns': ['34-0.0', '52-0.0'],
        'func': lambda df: concat_strings(df.astype('str'), sep='-'),
    },

    'DateOfDeath': {
        'columns': ['40000-0.0', '40000-1.0', '40000-2.0'],
        'func': lambda df: df.astype('datetime64').min(axis=1),
    },

    'SystolBloodPressur': {
        'columns': ['4080-0.0', '4080-0.1', '93-0.0', '93-0.1'],
        'func': lambda df: df.mean(axis=1),
    },

    'CauseOfDeath': {
        'columns': ['40001-0.0', '40001-1.0', '40001-2.0'],
        'func': lambda df: concat_strings(df, sep=","),
    },

    'SecondaryCauseOfDeath': {
        'columns': [f'40002-{i}.{j}' for i in range(3) for j in range(14)],
        'func': lambda df: concat_strings(df, sep=","),
    },

    'AgeAtDeath': {
        'columns': ['40007-0.0', '40007-1.0', '40007-2.0'],
        'func': lambda df: df.min(axis=1),
    },

}

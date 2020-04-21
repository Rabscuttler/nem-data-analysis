import numpy as _np
import pandas as _pd


def merge_duid_mappings(df, gen_loads, fcas):
    '''
    Provided a DataFrame that has DUID as an identifier,
    returns DataFrame with DUID identifiers merged in.
    Args:
        df (pandas DataFrame): dataframe with col "DUID"
        gen_loads (""): Generators and Scheduled Loads df
        fcas (""): Unique FCAS providers df
    Returns:
        Cleaned DataFrame with identifiers attached to DUID
    '''
    df = _pd.merge(df, gen_loads,
                   left_on='DUID', right_on='DUID',
                   how='left')
    df = _pd.merge(df, fcas,
                   left_on='DUID', right_on='DUID',
                   how='left')

    # consolidate duplicate columns
    duped_cols = ['Region', 'Participant', 'Station Name']
    for col in duped_cols:
        df[col] = _np.where(df[(col+'_x')].isna(),
                            df[(col+'_y')],
                            df[(col+'_x')])
        df = df.drop(columns=[col + '_x', col + '_y'])

    return df


def merge_causpays_mappings(df, elements, variables,
                            ems_duid=None, gen_loads=None):
    '''
    Provided a DataFrame containing Causer Pays 4s data,
    returns a DataFrame with element and variable
    identifiers merged in
    Args:
        df (pandas DataFrame): Causer Pays data with col names
                               'elementnumber' & 'variablenumber'
        elements (''): Causer Pays elements mapping as a df
        variables (''): '' variables mapping as a df
        ems_duid ('', optional): mapping between EMSNAME and DUID as a df
        gen_loads ('', optional): Generators and Scheduled loads
                                  (DUID identifiers). If this is supplied,
                                  provide ems_duid
    Retuns:
        DataFrame with element and variable identifiers
    '''
    # merge in Causer Pays elements and variables mappings
    df = _pd.merge(left=df, right=elements, how='left',
                   left_on='elementnumber', right_on='ELEMENTNUMBER')
    df = _pd.merge(left=df, right=variables, how='left',
                   left_on='variablenumber', right_on='VARIABLENUMBER')
    # map ems to duid and gen+load info if DataFrames provided

    if ems_duid is not None:
        df = df.drop('ELEMENTNUMBER', axis=1)
        df = _pd.merge(left=df, right=ems_duid, how='left',
                       on='EMSNAME')
    if gen_loads is not None:
        df = _pd.merge(left=df, right=gen_loads, how='left',
                       on='DUID')

    return df

import os as _os
import pandas as _pd

from nemosis import data_fetch_methods as _data_fetch_methods

_dummy_start = '2018/01/01 00:00:00'
_dummy_end = '2018/12/31 23:59:59'


def fetch_gen_scheduled_loads(raw_loc, table_loc, dummy_start, dummy_end):
    '''
    Fetches the Registration and Exemptions xlsx and returns the Generators
    and Scheduled Loads table

    Args:
        raw_loc (str or path): directory to save the raw xlsx
        table_loc (str or path): directory to save the G&L table as a csv
        dummy_start (str): dummy start dt as required by nemosis
        dummy_end (str): dummy end dt as required by nemosis

    Returns:
        Pandas DataFrame of Generators and Scheduled Loads table
    '''
    nemosis_table = 'Generators and Scheduled Loads'
    df = _data_fetch_methods.static_table_xl(start_time=dummy_start,
                                             end_time=dummy_end,
                                             table_name=nemosis_table,
                                             raw_data_location=raw_loc)
    df.to_csv(_os.path.join(table_loc, 'generators_and_loads.csv'),
              index=False)

    return df


def fetch_ancillary_service_providers(reg_exemps_xlsx_loc, table_loc=None):
    '''
    Looks at the Ancillary Services tab of the Registration and Exemptions xlsx
    and returns the Ancillary Service providers table, which includes all
    ancillary services providers

    Args:
        reg_exemps_xlsx_loc (str or path): directory where NEM Reg&Exemp.xlsx
                                           is located.
        table_loc (str or path): directory to save the Ancillary Services table

    Returns:
        Pandas DataFrame of Generators and Scheduled Loads table
    '''
    reg_exemps = _os.path.join(reg_exemps_xlsx_loc,
                               'NEM Registration and Exemption List.xls')
    df = _pd.read_excel(reg_exemps, sheet_name='Ancillary Services')

    df.dropna(axis=1, how='all', inplace=True)
    df.drop(columns=['Unnamed: 11'], inplace=True)

    df.to_csv(_os.path.join(table_loc, 'ancillary_service_providers.csv'),
              index=False)

    return df


def clean_gen_loads_tech(gen_loads_path=None, df=None, table_loc=None,
                         outname='generators_and_loads.csv'):
    '''
    Registration and Exemptions list contain various technology types
    Some of these are repeated (difference of case or a few words)
    Take generators and scheduled loads csv and
    cleans technology types based on mapping in this function

    Args:
        gen_loads_path (str or pat, optional): Directory containing G&L csv
        df (pd.DataFrame, optional): provide df instead of path to csv
        table_loc (str or path, optional): path to save cleaned table
        outname (str, optional): used if table_loc provided

    Returns:
        Pandas Dataframe with condensed tech types
    '''
    condensed_techs = {
                       'Battery and Inverter': 'Battery',
                       'Combined Cycle Gas Turbine (CCGT)': 'CCGT',
                       'Photovoltaic Flat panel': 'PV',
                       'Photovoltaic Tracking  Flat Panel': 'PV',
                       'Photovoltaic Tracking Flat Panel': 'PV',
                       'Photovoltaic Tracking Flat panel': 'PV',
                       'Wind - Onshore': 'Wind',
                       'Pump Storage': 'Pump/Load',
                       '-': 'Pump/Load'
                   }
    replace = (lambda x: condensed_techs[x]
               if x in condensed_techs.keys() else x)
    if gen_loads_path:
        df = _pd.read_csv(_os.path.join(gen_loads_path,
                          'generators_and_loads.csv'))
    df['Technology Type - Descriptor'] =\
        df['Technology Type - Descriptor'].apply(replace)

    if table_loc:
        csv_path = _os.path.join(table_loc, outname)
        df.to_csv(csv_path, index=False)

    return df


def clean_gen_loads_capacities(gen_loads_path=None, df=None, table_loc=None,
                               outname='generators_and_loads.csv'):
    '''
    Each row in the Generators and Loads list corresponds to a
    unit. Each unit has various capacities (MW).
    Reg Cap (MW) is believed to correspond to unit capacities.
    This function cleans any null values and returns a
    dataframe with numerical capacities.
    Args:
        gen_loads_path (str or pat, optional): Directory containing G&L csv
        df (pd.DataFrame, optional): provide df instead of path to csv
        table_loc (str or path, optional): path to save cleaned table
        outname (str, optional): used if table_loc provided

    Returns:
        Pandas Dataframe with cleaned capacities
    '''
    if gen_loads_path:
        df = _pd.read_csv(_os.path.join(gen_loads_path,
                          'generators_and_loads.csv'))
    df['Reg Cap (MW)'] = df['Reg Cap (MW)'].str.replace('-', '0')
    df['Reg Cap (MW)'] = df['Reg Cap (MW)'].astype('float64')

    if table_loc:
        csv_path = _os.path.join(table_loc, outname)
        df.to_csv(csv_path, index=False)
    return df


def find_unique_fcas_providers(gen_loads_path, ancillary_services_path,
                               table_loc=None):
    '''
    Some DUIDs map to market ancillary service providers.
    This function identifies these DUIDs and returns
    a dataframe with basic information about the DUID.

    Args:
        gen_loads_path (str or path): Directory containing G&L csv
        ancillary_services_path (str or path): Dir containing ASP csv
        table_loc (str or path, optional): path to save table with providers

    Returns:
        Pandas Dataframe with unique fcas providers and basic info
    '''
    asp_path = _os.path.join(ancillary_services_path,
                             'ancillary_service_providers.csv')
    gen_load_path = _os.path.join(gen_loads_path,
                                  'generators_and_loads.csv')
    fcas_providers = _pd.read_csv(asp_path)
    gen_load = _pd.read_csv(gen_load_path)

    unique_fcas = set(fcas_providers['DUID']) - set(gen_load['DUID'])
    unique_fcas_providers = \
        fcas_providers[fcas_providers['DUID'].isin(unique_fcas)]
    unique_fcas_providers = \
        unique_fcas_providers[~unique_fcas_providers['DUID'].isna()]
    fcas_provider_cols = ['DUID', 'Region', 'Participant', 'Station Name']
    unique_fcas_providers = \
        unique_fcas_providers.drop_duplicates(fcas_provider_cols)
    unique_fcas_providers = unique_fcas_providers[fcas_provider_cols]

    if table_loc:
        save_path = _os.path.join(table_loc, 'unique_fcas_providers.csv')
        unique_fcas_providers.to_csv(save_path, index=False)

    return unique_fcas_providers

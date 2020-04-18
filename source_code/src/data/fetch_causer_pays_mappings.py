import argparse as _argparse
import logging as _logging
import os as _os
import pandas as _pd
from shutil import rmtree as _rmtree

from src.data.nem_participants import _dummy_start, _dummy_end
from nemosis.data_fetch_methods import static_table as _static_fetch


def create_parser():
    description = ("Fetch causer pays mapping tables into path")
    parser = _argparse.ArgumentParser(description=description)
    parser.add_argument('-path', type=str, required=True,
                        help='path to save fetched raw files')
    args = parser.parse_args()
    return args


_logging.basicConfig(format='\n%(levelname)s:%(message)s',
                     level=_logging.INFO)
args = create_parser()
raw_loc = args.path
tmp_dir = _os.path.join(raw_loc, 'tmp')

_os.mkdir(tmp_dir)
elements = _static_fetch(start_time=_dummy_start, end_time=_dummy_end,
                         table_name='ELEMENTS_FCAS_4_SECOND',
                         raw_data_location=tmp_dir)

variables = _static_fetch(start_time=_dummy_start, end_time=_dummy_end,
                          table_name='VARIABLES_FCAS_4_SECOND',
                          raw_data_location=tmp_dir)

elements.to_csv(_os.path.join(raw_loc, 'elements_causpays_mapping.csv'),
                index=False)
variables.to_csv(_os.path.join(raw_loc, 'variables_causpays_mapping.csv'),
                 index=False)
_rmtree(tmp_dir)

_logging.info(f'FCAS mappings in {raw_loc}')

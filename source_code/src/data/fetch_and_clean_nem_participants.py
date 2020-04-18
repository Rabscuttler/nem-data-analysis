import argparse as _argparse
import logging as _logging

from src.data import nem_participants as _nem_p
from src.data.nem_participants import _dummy_start
from src.data.nem_participants import _dummy_end


def create_parser():
    description = ("Fetch participant tables into project data directories")
    parser = _argparse.ArgumentParser(description=description)
    parser.add_argument('-raw_path', type=str, required=True,
                        help='path to save fetched raw files')
    parser.add_argument('-proc_path', type=str, required=True,
                        help='path to save cleaned files')
    args = parser.parse_args()
    return args


_logging.basicConfig(format='\n%(levelname)s:%(message)s',
                     level=_logging.INFO)

args = create_parser()
raw_path = args.raw_path
proc_path = args.proc_path
gen_loads_outname = 'cleaned_gen_loads.csv'
# fetch raw generators and loads and clean, then save to processed path
raw_gen_loads = _nem_p.fetch_gen_scheduled_loads(raw_path, raw_path,
                                                 _dummy_start, _dummy_end)
cleaned_tech = _nem_p.clean_gen_loads_tech(df=raw_gen_loads)
clean_tech_cap = _nem_p.clean_gen_loads_capacities(df=cleaned_tech,
                                                   table_loc=proc_path,
                                                   outname=gen_loads_outname)
_logging.info((f'Raw Gen and Load files in {raw_path},'
               + 'processed in {proc_path}'))

# fetch fcas providers then find unique providers
fcas_providers = _nem_p.fetch_ancillary_service_providers(raw_path,
                                                          table_loc=raw_path)
unique_fcas = _nem_p.find_unique_fcas_providers(raw_path, raw_path,
                                                table_loc=proc_path)
_logging.info(f'FCAS providers in {raw_path}, unique providers in {proc_path}')

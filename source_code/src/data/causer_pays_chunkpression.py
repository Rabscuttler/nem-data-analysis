import argparse
import logging
import os
import tqdm

import numpy as np
import pandas as pd

from sys import getsizeof


def arg_parser():
    description = ("Merge FCAS data in directories to parquet chunks.\n"
                   + "Indexed on sorted datetime column to improve Dask speed")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-path', type=str, required=True,
                        help='recursive search for files with format in path')
    parser.add_argument('-format', type=str, required=True,
                        help='.{format} to search for. csv or parquet')
    parser.add_argument('-memory_limit', type=int, required=True,
                        help=('memory (MB) before file write.'
                              + ' Recommended RAM/2'))
    args = parser.parse_args()
    return args


def pathfiles_to_chunks(path, fformat, mem_limit):
    read_files = walk_dirs_for_files(path, fformat)
    concat_list = []
    concat_df = pd.DataFrame()
    i = 0
    mem = 0
    for file in tqdm.tqdm(read_files, desc='Reading file:'):
        df = read_dataframes(fformat, file)
        concat_list.append(df)
        df_mem = getsizeof(df)
        mem += df_mem / 1e6
        if mem < mem_limit:
            logging.info(f'Memory: {mem}')
        elif mem >= mem_limit:
            concat_df = pd.concat(concat_list)
            concat_df = concat_df.sort_index()
            chunk_name = path + os.sep + f'chunk{i}.parquet'
            concat_df.to_parquet(chunk_name)
            logging.info(f'Writing chunk {chunk_name}')
            i += 1
            concat_list = []
            concat_df = pd.DataFrame()
            mem = 0

    final_mem = concat_df.memory_usage().sum() / 1e6
    if final_mem > 0:
        chunk_name = path + os.sep + f'chunk{i}.parquet'
        concat_df.to_parquet(chunk_name)
        logging.info(f'Writing chunk {chunk_name}')


def walk_dirs_for_files(path, fformat):
    read_files = []
    for root, subs, files in os.walk(path):
        if files:
            logging.info(f' Reading files in {root}')
            flist = [root + os.sep + x for x in files if fformat in x.lower()]
            if flist:
                read_files.extend(flist)
    if not read_files:
        logging.error(' Check path and format. No files to read')
        raise argparse.ArgumentError()
    else:
        return sorted(read_files)


def read_dataframes(fformat, path):
    original_cols = ['TIMESTAMP', 'ELEMENTNUMBER', 'VARIABLENUMBER',
                     'VALUE', 'VALUEQUALITY']
    cols = ['datetime', 'elementnumber', 'variablenumber',
            'fcas_value', 'valuequality']
    if fformat == 'csv':
        df = pd.read_csv(path)
        verfied_cols = df.columns[df.columns.isin(original_cols)]
        df = df[verfied_cols]
        if len(verfied_cols) == 0:
            df = pd.read_csv(path, header=None)
        elif len(verfied_cols) < len(original_cols):
            raise ValueError("Causer Pays data missing some columns")
    elif fformat == 'parquet':
        df = pd.read_parquet(path)
    df.columns = cols
    df['datetime'] = df['datetime'].astype(np.datetime64)
    df = df.set_index('datetime')
    return df


def main():
    logging.basicConfig(format='\n%(levelname)s:%(message)s',
                        level=logging.INFO)
    args = arg_parser()
    pathfiles_to_chunks(args.path, args.format, args.memory_limit)


if __name__ == "__main__":
    main()

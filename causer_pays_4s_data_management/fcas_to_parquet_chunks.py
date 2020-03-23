import argparse
import logging
import os
import tqdm

import pandas as pd


def arg_parser():
    description = ("Merge FCAS data in directories to parquet chunks")
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
    concat_df = pd.DataFrame()
    i = 0
    for file in tqdm.tqdm(read_files, desc='Reading file:'):
        df = read_dataframes(fformat, file)
        mem = concat_df.memory_usage().sum() / 1e6
        if mem < mem_limit:
            concat_df = pd.concat([concat_df, df])
            logging.info(f'Memory: {mem}')
        elif mem >= mem_limit:
            chunk_name = path + os.sep + f'chunk{i}.parquet'
            concat_df.to_parquet(chunk_name)
            logging.info(f'Writing chunk {chunk_name}')
            i += 1
            concat_df = pd.DataFrame()

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
        return read_files


def read_dataframes(fformat, path):
    cols = ['datetime', 'elementnumber', 'variablenumber',
            'fcas_value', 'valuequality']
    if fformat == 'csv':
        df = pd.read_csv(path, header=None)
    elif fformat == 'parquet':
        df = pd.read_parquet(path)
    df.columns = cols
    return df


def main():
    logging.basicConfig(format='\n%(levelname)s:%(message)s',
                        level=logging.INFO)
    args = arg_parser()
    pathfiles_to_chunks(args.path, args.format, args.memory_limit)


if __name__ == "__main__":
    main()

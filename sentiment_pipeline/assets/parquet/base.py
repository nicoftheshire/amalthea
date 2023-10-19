# File name: base.py
# The purpose of this code is to simulate the reading of data into the parquet
"""
File name: base.py

This is the source code that implements the reading of data into a parquet.
It occurs after the sentiment analysis part of the data pipeline and uses
pandas to read and write data to and from the parquet. Since a parquet file's
data is stored per column, accessing a data point according to properties is
much faster.

"""
import json

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np


def create_dataset(size):
    """
    Creates a dataset with fields 'date', 'source', 'score', and 'currency',
    which are all randomly populated.

    Parameters
    ----------
    size: int
        the number of entries in the dataset
    """

    df = pd.DataFrame()
    dates = pd.date_range('2023-01-01', '2023-08-01')

    df['date'] = np.random.choice(dates, size)
    df['source'] = np.random.choice(['bbc', 'the-verge', 'reuters'], size)
    df['score'] = np.random.uniform(0, 1, size)
    df['currency_pair'] = np.random.choice(['USD/ZAR', 'USD/JPY', 'ZAR/JPY'], size)

    return df


def set_types(df):
    """
    Sets the types of the dataset fields for faster reading and writing. These
    fields are subject to change throughout the project.

    Parameters
    ----------
    df: pandas.DataFrame
        the df for which the types are being set
    """

    df['date'] = df['date'].astype('string')
    pd.to_datetime(df['date'])
    df['source'] = df['source'].astype('string')
    df['score'] = df['score'].astype('float32')
    df['currency_pair'] = df['currency_pair'].astype('string')

    return df


def read_data(file_path):
    """
    Creates a dataframe from the json file received from the sentiment analysis
    part of the pipeline.

    Parameters
    ----------
    file_path: string
        path to the json file
    """

    df = pd.DataFrame(columns=['date', 'source', 'score', 'currency_pair'])
    df = set_types(df)
    df = pd.read_json(file_path)

    return df


def store_parquet():
    """
    Called from the pipeline. Appends the received entries to the parquet.
    """
    # This code can be used to create the df from the json file - it probably
    # needs some changes depending on our needs.

    # new_data = read_data('analyze_data.json')
    new_data = pd.read_json('analyze_data.json')

    try:
        existing_data = pd.read_parquet('sentiment_analysis_data.parquet')
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    combined_data.to_csv('sentiment_analysis_data.csv')

    table = pa.Table.from_pandas(combined_data)
    pq.write_table(table, 'sentiment_analysis_data.parquet')

    # df = create_dataset(100)
    # df = set_types(df)
    # df.to_csv('output.csv')

    # table = pa.Table.from_pandas(df)
    # pq.write_table(table, 'output.parquet', version='1.0')

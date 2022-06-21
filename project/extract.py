import logging

import pandas as pd


def download_csv_file(url: str) -> pd.DataFrame:
    """Download a CSV file from the Web to use it
    as a Pandas DataFrame.

    Parameters
    ----------
    url : str
        Web URL to look for the file.

    Returns
    -------
    df : pd.DataFrame
        The resulting DataFrame from the csv file.

    """
    try:
        logging.info(f"Downloading data from CSV file...")
        df = pd.read_csv(url)
        return df
    except Exception as e:
        raise Exception(e)

import logging
from pathlib import Path

import pandas as pd
import sqlalchemy

from project.constants import TEMP_DIR
from project.load import save_df_to_csv
from project.schemas import csv_columns_data


def get_uri_db_pg(db_cfg: dict) -> str:
    """Build SQLAlchemy URI

    Parameters
    ----------
    db_cfg : dict
        Database credentials.
        It has the following keys:
            - dialect
            - driver
            - username
            - password
            - host
            - port
            - database

    Returns
    -------
    uri_db : str
        Connection string of SqlAlchemy

    """
    uri_db = f"{db_cfg['dialect']}+{db_cfg['driver']}://{db_cfg['username']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['database']}"  # noqa: E501
    if db_cfg["dialect"] == "mssql":
        uri_db += "?driver=ODBC+Driver+17+for+SQL+Server"
    return uri_db


def build_db_engine(db_cfg: dict) -> sqlalchemy.engine.Engine:
    """Function to build a SQLAlchemy engine for reading/loading
    data from/to the desired DB.

    Parameters
    ----------
    db_cfg : dict
        Database credentials.
        It has the following keys:
            - dialect
            - driver
            - username
            - password
            - host
            - port
            - database

    Returns
    -------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine instance.

    """
    db_location = get_uri_db_pg(db_cfg)
    assert isinstance(db_location, str), "Bad Database location"

    engine = sqlalchemy.create_engine(db_location)
    assert isinstance(
        engine, sqlalchemy.engine.Engine
    ), "DB engine could not be created."

    return engine


def cleanup_files():
    """
    Clean temporary csv files located in temp folder.

    """
    logging.info("Cleaning csv files..")
    for f in Path(TEMP_DIR).glob("*.csv"):
        logging.info(f"Removing {f} ..")
        f.unlink()
    logging.info("All csv files cleaned.")


def format_temp_files():
    """
    Create csv files for temporary save of the required data.

    """
    for key in csv_columns_data:
        df = pd.DataFrame(columns=list(csv_columns_data[key]))
        save_df_to_csv(df, TEMP_DIR, key, "w", True)

from pathlib import Path

import pandas as pd

from project.cfg import SQL_SERVER_CFG
from project.constants import CSV_URL, DB_TABLE_NAME, TEMP_DIR
from project.extract import download_csv_file
from project.load import load_df, mount_db_backup
from project.validate import validate_loaded_data


def load_dfs():
    """
    Persist every DataFrame from our temp csv files to the
    desired database and check for any inconsistency.

    """
    for f in Path(TEMP_DIR).glob("*.csv"):
        df = pd.read_csv(f)

        load_df(df, db_cfg=SQL_SERVER_CFG, table=DB_TABLE_NAME, add_copy_date=True)
        validate_loaded_data(df, db_cfg=SQL_SERVER_CFG, table=DB_TABLE_NAME)


def main():
    # Mount DB Backup
    mount_db_backup(db_cfg=SQL_SERVER_CFG)

    # Download CSV
    df = download_csv_file(CSV_URL)

    # Insert to table including addition date
    load_df(df, db_cfg=SQL_SERVER_CFG, table=DB_TABLE_NAME, add_copy_date=True)

    # Test for no information loss
    validate_loaded_data(df, db_cfg=SQL_SERVER_CFG, table=DB_TABLE_NAME)


if __name__ == "__main__":
    main()

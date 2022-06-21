import logging
import subprocess

import pandas as pd

from project.cfg import SQL_SERVER_PASSWORD, SQL_SERVER_USER
from project.constants import COLUMNS_TO_COMPARE_DUPLICATES, DATA_DIR, TEMP_DIR
from project.helpers import build_db_engine
from project.transform import add_date_to_dataframe, remove_duplicates_from_dataframe


def load_df(df: pd.DataFrame, db_cfg: dict, table: str, add_copy_date: bool) -> None:
    """Persist a DataFrame to a table in a specified Database.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to load.

    db_cfg : dict
        DB Credentials constant taken from config file.
        Example: SQL_SERVER_CFG.

    table : str
        Name of the table to upload the data.

    add_copy_date : bool
        Flag to indicate if the addition date should be included in the DataFrame.

    """
    engine = build_db_engine(db_cfg)

    actual_records_df = pd.read_sql_table(
        f"{table}", engine, columns=COLUMNS_TO_COMPARE_DUPLICATES
    )

    clean_sorted_df = remove_duplicates_from_dataframe(
        df,
        sort_columns=[COLUMNS_TO_COMPARE_DUPLICATES[0]],
        columns=COLUMNS_TO_COMPARE_DUPLICATES,
        keep="last",
    )
    merge_df = actual_records_df.merge(
        clean_sorted_df, on=COLUMNS_TO_COMPARE_DUPLICATES, how="right", indicator=True
    )
    new_records_df = merge_df[merge_df._merge == "right_only"]

    if add_copy_date:
        new_records_df = add_date_to_dataframe(new_records_df, "fecha_copia")

    new_records_df.to_sql(f"{table}", engine, index=False, if_exists="append")

    new_records_count = len(new_records_df.index)
    logging.info(
        f"{new_records_count} records from CSV loaded into DB table {table} successfully."
    )


def mount_db_backup(db_cfg: dict) -> None:
    """Check if the DB already exists in the SQL Server. If it doesn't,
    mount the backup into the server to start loading records.

    Parameters
    ----------
    db_cfg : dict
        DB Credentials constant taken from config file.
        Example: SQL_SERVER_CFG.

    """
    engine = build_db_engine(db_cfg)

    db_names_df = pd.read_sql("SELECT name FROM sys.databases", engine)

    if "dbo" in db_names_df.name:
        logging.info("DBO database already in SQL Server. Skipping backup mount...")
        return
    else:
        backup_path = DATA_DIR / "testing_etl.bak"
        try:
            subprocess.run(
                [
                    "sh",
                    f"sqlcmd -S localhost -U {SQL_SERVER_USER} -P {SQL_SERVER_PASSWORD} -Q  'RESTORE DATABASE [dbo] FROM DISK = N{backup_path} WITH FILE = 1, NOUNLOAD, REPLACE, STATS = 5",
                ]
            )
            logging.info("Backup mounted successfully.")
            return
        except Exception as e:
            logging.info(
                f"{e}. Could not mount db backup. Check your configuration and try again."
            )
            return


def save_df_to_csv(
    df: pd.DataFrame, dir: str, file_name: str, mode: str, header: bool
) -> None:
    """Save data in desired mode from a DataFrame to a CSV file
    in the specified directory, with the option of writing the file headers.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to save into the csv file.

    dir : str
        The directory to save the csv.

    file_name : str
        The file name to save the csv.

    mode : str
        The open mode to work with the file ("a", "w", etc.).

    header : bool
        Flag to indicate if the DataFrame headers should be written.

    """
    logging.info(f"Writing in {mode} mode the {file_name} DataFrame to csv..")
    with open(f"{dir}/{file_name}.csv", f"{mode}") as outfile:
        df.to_csv(path_or_buf=outfile, index=False, header=header)

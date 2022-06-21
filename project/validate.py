import logging

import pandas as pd

from project.constants import COLUMNS_TO_COMPARE_DUPLICATES
from project.helpers import build_db_engine
from project.transform import remove_duplicates_from_dataframe


def validate_loaded_data(df: pd.DataFrame, db_cfg: dict, table: str) -> None:
    """Validate if data from the DataFrame has been loaded to
     the specified database and table.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to compare.

    db_cfg : dict
        DB Credentials constant taken from config file.
        Example: SQL_SERVER_CFG.

    table : str
        Name of the table to compare.

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

    inner_merge_df = actual_records_df.merge(
        clean_sorted_df, how="inner", on=COLUMNS_TO_COMPARE_DUPLICATES
    )

    if len(clean_sorted_df.index) == len(inner_merge_df.index):
        logging.info(
            f"Data from the passed DataFrame is in the {table} table. Exiting..."
        )
        return
    elif len(clean_sorted_df.index) > len(inner_merge_df.index):
        logging.info(
            f"Not all data from the passed DataFrame could be found in the {table} table."
        )
        raise Exception("DatabaseLoadError")

import pandas as pd


def add_date_to_dataframe(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Add today's date to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Web URL to look for the file.

    column_name : str
        Column where the date should be added.

    Returns
    -------
    df : pd.DataFrame
        The resulting DataFrame with the date added into the specified column.

    """
    df[f"{column_name}"] = pd.to_datetime("today")
    return df


def remove_duplicates_from_dataframe(
    df: pd.DataFrame,
    sort_columns: list | None = None,
    columns: list | None = None,
    keep: str | None = False,
) -> pd.DataFrame:
    """Remove duplicates from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to drop duplicates.

    sort_columns : list | None
        List of columns to sort the DataFrame before removing duplicates.

    columns : list | None
        List of columns to compare for duplicates.

    keep : str | None
        Determines which duplicates (if any) to keep.

    Returns
    -------
    clean_df : pd.DataFrame
        The resulting DataFrame with the duplicates removed.

    """
    clean_df = df.sort_values(by=sort_columns).drop_duplicates(
        subset=columns, keep=keep
    )
    return clean_df

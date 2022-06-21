from decouple import AutoConfig

from project.constants import REPO_ROOT

config = AutoConfig(search_path=REPO_ROOT)

SQL_SERVER_CFG = {
    "dialect": config("SQL_SERVER_DIALECT", default="mssql", cast=str),
    "driver": config("SQL_SERVER_DRIVER", default="pyodbc", cast=str),
    "username": config("SQL_SERVER_USER", default="sa", cast=str),
    "password": config("SQL_SERVER_PASSWORD", default="password", cast=str),
    "host": config("SQL_SERVER_HOST", default="sql-server-db", cast=str),
    "port": config("SQL_SERVER_PORT", default=1433, cast=int),
    "database": config("SQL_SERVER_DB", default="db", cast=str),
}
SQL_SERVER_USER = config("SQL_SERVER_USER", default="sa", cast=str)
SQL_SERVER_PASSWORD = config("SQL_SERVER_PASSWORD", default="password", cast=str)

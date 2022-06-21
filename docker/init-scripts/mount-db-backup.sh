#!/bin/bash
# Script to mount the backup file. Not environment variables can be changed as you like.

sqlcmd -S localhost -U $SQL_SERVER_USER -P $SQL_SERVER_PASSWORD -Q  "RESTORE DATABASE [dbo] FROM DISK = N'/var/opt/mssql/data/testing_etl.bak' WITH FILE = 1, NOUNLOAD, REPLACE, STATS = 5"

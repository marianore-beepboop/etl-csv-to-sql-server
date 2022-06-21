# ETL Process to download a CSV file and add new registers to a SQL Server DB

The repository shows a way to make a scheduled ETL process where we
download a web-hosted CSV and insert the new registers into a SQL Server DB.
We compare with the DB table for duplicates before inserting and also add a record
with the addition date of the row (optional). There's also the option to mount a
personal backup of the DB Server before making any changes.
Depending on how you run the project you can read logs with a .txt file or within the
Apache Airflow UI.

You can easily modify any configuration as you like with minimal modifications needed.
DB Server preference, URLs, variable naming, directory locations, IPs, Crons, etc.
This is just a template for you to play on.

## How to run the project

### Running the project with docker compose

1. Change directory into `project/docker`.
2. Build the project Dockerfile by running `run docker-compose --env-file ../.env build`
3. Run `docker-compose --env-file ../.env up --build`
4. Enter Airflow with localhost:2021 (replace localhost with your Cloud External IP, if applicable)

### Running the project with minimal compute hardware

You may not want to run a containerized environment and just update the DB every week.
You can do so by following the instructions below:

You can use `crontab` to schedule your Python scripts to run.
The parameters you'll need are:

- Your cron expression (you can use [Crontab Guru](https://crontab.guru/) to easily obtain it)
- Your python executable absolute path.
- Your python script absolute path.

Type `crontab -e` and add a row inside the editor for each cron job you want.
Example:
`0 5 * * 1 /root/.cache/pypoetry/virtualenvs/project-py3.9/bin/python /Users/mariano/project/main.py`
After saving the file you now can preview your scheduled jobs with `crontab -l`.

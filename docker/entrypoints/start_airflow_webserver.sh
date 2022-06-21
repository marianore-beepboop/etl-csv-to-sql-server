#!/bin/bash
# Script that allows the users and connections creations for Airflow service.

poetry run airflow db init

poetry run airflow db upgrade

if [ "$AIRFLOW_CREATE_USER_CONN" = true ]; then
    # Create User
    echo "Creating airflow user..."
    poetry run airflow users create -r "$AIRFLOW_ROLE" -u "$AIRFLOW_USER" -p "$AIRFLOW_PASSWORD" -f "$AIRFLOW_FIRST" -l "$AIRFLOW_LAST" -e "$AIRFLOW_EMAIL"
fi

# Create connection to Slack to receive alerts within the App.
poetry run airflow connections add "slack_connection" \
    --conn-type "http" \
    --conn-password "$AIRFLOW_CONNECTION_SLACK_PASSWORD" \
    --conn-host "$AIRFLOW_CONNECTION_SLACK_HOST_URL"

poetry run airflow webserver

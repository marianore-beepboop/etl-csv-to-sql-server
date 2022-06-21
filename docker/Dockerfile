FROM python:3.9

# Setup pipx and poetry
RUN pip install pipx
RUN pipx install poetry
ENV PATH="/root/.local/pipx/venvs/poetry/bin/:$PATH"

COPY data/testing_etl.bak /var/opt/mssql/data/testing_etl.bak

COPY pyproject.toml poetry.lock /tmp/
RUN poetry install --no-root --no-interaction

COPY . /project/
WORKDIR /project/
RUN poetry install --no-interaction

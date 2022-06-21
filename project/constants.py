"""Collection of constants that are reutilized over the entire project to avoid repetition."""
from pathlib import Path

from pkg_resources import resource_filename

_p = Path(resource_filename("project", "/"))

PROJECT_PATH = _p / "project"
REPO_ROOT = PROJECT_PATH.parent
RESOURCES_PATH = _p / "resources"
DATA_DIR = _p / "data"
DOCKER_DIR = _p / "docker"
LOGS_DIR = _p / "logs"
SCRIPTS_DIR = DOCKER_DIR / "init-scripts"
TEMP_DIR = DATA_DIR / "temp"

CSV_URL = "https://francisadbteststorage.blob.core.windows.net/challenge/nuevas_filas.csv?sp=r&st=2021-07-08T18:53:40Z&se=2022-12-09T02:53:40Z&spr=https&sv=2020-08-04&sr=b&sig=AK7dCkWE1xR28ktHfdSYU2RSZITivBQmv83U51pyJMo%3D"
DB_TABLE_NAME = "Unificado"
COLUMNS_TO_COMPARE_DUPLICATES = ["id", "muestra", "resultado"]

import os
from urllib.parse import quote_plus
from .helpers import is_missing_env_vars

from logging import getLogger
logger = getLogger(__name__)
LOG = f"{__name__}-"


def find_odbc_driver():
    import pyodbc
    drivers = [driver for driver in pyodbc.drivers() if driver.startswith("ODBC")]

    if len(drivers) == 0:
        raise Exception("Failed to find odbc driver.")

    return drivers[-1]


def add_sql_database_env_vars(config_class, prefix: str = "DATABASE"):
    env_vars = [
        f"{prefix}_SERVER",
        f"{prefix}_NAME",
        f"{prefix}_USERNAME",
        f"{prefix}_PASSWORD",
    ]

    # Check for missing variables
    if is_missing_env_vars(env_vars=env_vars):
        return None, None

    config_class.add_env_vars_to_self(env_vars)

    return make_sql_database_uris(config_class, prefix=prefix)


def make_sql_database_uris(config_class, prefix: str = "DATABASE"):
    pyodbc_uri_name = f"SQLPYODBC_{prefix}_URI"
    sqlalchemy_uri_name = f"SQLALCHEMY_{prefix}_URI"

    # Determine which ODBC driver is installed
    odbc_driver_name = find_odbc_driver()
    logger.info(f"{LOG} Found ODBC driver with name '{odbc_driver_name}'.")

    pyodbc_uri = (
            f"DRIVER={{{odbc_driver_name}}};"
            + f"SERVER={os.environ.get(prefix + '_SERVER').replace(':', ',')};"
            + f"DATABASE={os.environ.get(prefix + '_NAME')};"
            + f"UID={os.environ.get(prefix + '_USERNAME')};"
            + f"PWD={os.environ.get(prefix + '_PASSWORD')}"
    )

    sqlalchemy_uri = (
            f"mssql+pyodbc://{quote_plus(os.environ.get(prefix + '_USERNAME'))}:"
            + f"{quote_plus(os.environ.get(prefix + '_PASSWORD'))}"
            + f"@{os.environ.get(prefix + '_SERVER')}/{os.environ.get(prefix + '_NAME')}"
            + f"?driver={odbc_driver_name.replace(' ', '+')}"
    )

    os.environ[pyodbc_uri_name] = pyodbc_uri
    os.environ[sqlalchemy_uri_name] = sqlalchemy_uri

    setattr(config_class, pyodbc_uri_name, pyodbc_uri)
    setattr(config_class, sqlalchemy_uri_name, sqlalchemy_uri)

    return pyodbc_uri, sqlalchemy_uri

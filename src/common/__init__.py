import os
from urllib.parse import quote_plus
from logging import getLogger
from dotenv import load_dotenv

# Start logging at the console based on the name of this file
logger = getLogger(__name__)
LOG = f"{__name__}-"

# This will load the .env file as environment variables.
load_dotenv()

ODBC_DRIVER_NAME = ''


class Config(object):
    def __init__(self):
        self.DATABASE_SERVER = self.get_env_var('DATABASE_SERVER')
        self.DATBASE_NAME = self.get_env_var('DATBASE_NAME')
        self.DATABASE_USERNAME = self.get_env_var('DATABASE_USERNAME')
        self.DATABASE_PASSWORD = self.get_env_var('DATABASE_PASSWORD')
        self.DATBASE_SQLALCHEMY_URI = self.build_sqlalchemy_uri()

    def build_sqlalchemy_uri(self):
        return f"mssql+pyodbc://{quote_plus(os.environ.get('DATABASE_USERNAME'))}:" + \
            f"{quote_plus(os.environ.get('DATABASE_PASSWORD'))}" + \
            f"@{os.environ.get('DATABASE_SERVER')}/{os.environ.get('DATBASE_NAME')}" + \
            f"?driver={ODBC_DRIVER_NAME.replace(' ', '+')}"
        
    def get_env_var(self, env_name):
        return os.getenv(env_name, None)
    


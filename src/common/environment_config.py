import os
import pathlib
from dotenv import load_dotenv

from logging import getLogger

logger = getLogger(__name__)
LOG = f"{__name__}-"

def find_common_env_file(
    base_dir: pathlib.Path = None,
    dotenv_path: pathlib.Path = None,
) -> pathlib.Path:
    # TODO: To handle multithreading, look for guid in env var, if not found, regen.

    if dotenv_path is None:
        paths = [base_dir] + [
            pathlib.Path(path)
            for path in os.environ.get("PYTHONPATH", "").split(os.pathsep)
        ]

        for path in paths:
            common_dotenv_path = path.joinpath(".env")

            if common_dotenv_path.exists():
                break

    if dotenv_path.exists():
        logger.info(f"{LOG} Located .env file at {dotenv_path}")
        return dotenv_path
    else:
        logger.info(f"CONFIG: Unable to locate .env file at {dotenv_path}")
        logger.info(
            "CONFIG: Does the common .env exist and did you enable the workspace?"
        )
        return None
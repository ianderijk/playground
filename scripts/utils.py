import os
import subprocess
import logging
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent.parent

logger = logging.Logger("playground", level="DEBUG")
file_handler = logging.FileHandler(ROOT / "playground.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def run_command(command: str, check: bool = True, logger=logger) -> Any:
    logger.debug(f"Running command '{command}'...")
    try:
        result = subprocess.run(
            command, shell=True, check=check, text=True, capture_output=True
        )
        logger.info("Command run successfully")
        return result
    except subprocess.CalledProcessError as e:
        logger.critical(f"Failed to run command, exception: {e}")
        os._exit(1)

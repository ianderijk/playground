import os
import subprocess
import time
import logging
from pathlib import Path
from typing import Any

logger = logging.Logger("playground-restore", level="DEBUG")
file_handler = logging.FileHandler(Path(__file__).parent / "playground.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.debug("Starting playground restoration")

NETWORK_NAME = "playground-routing"
SERVICE_GROUPS = ("core", "storage", "apis", "apps")
ROOT = Path(__file__).parent.absolute()


def run_command(command: str, check: bool = True) -> Any:
    logger.debug(f"Running command '{command}'...")
    try:
        result = subprocess.run(command, shell=True, check=check, text=True, capture_output=True)
        logger.info("Command run successfully")
        return result
    except subprocess.CalledProcessError as e:
        logger.critical(f"Failed to run command, exception: {e}")
        os._exit(1)


def check_env_files() -> None:
    logger.debug("Checking for env files...")
    envs_dir = ROOT / "environments"
    env_files = os.listdir(envs_dir)
    if sorted(env_files) != ["global.env", "secrets.env"]:
        logger.critical("Failed to find env files")
        os._exit(1)
    logger.info("Found env files")


def create_docker_network() -> None:
    logger.debug("Checking for docker network...")
    network_check = run_command(f"docker network inspect {NETWORK_NAME}", check=False)
    if network_check.returncode == 1:
        logger.debug(f"No network found, creating {NETWORK_NAME}...")
        run_command(f"docker network create {NETWORK_NAME}")
        logger.info("Network created")
        return
    logger.info("Network found")


def _find_compose_files() -> dict[str, list]:
    logger.info("Finding compose files...")
    compose_files = {k: [] for k in SERVICE_GROUPS}
    for service in SERVICE_GROUPS:
        service_path = ROOT / service
        for root, _, files in os.walk(service_path):
            if any("docker-compose" in x for x in files):
                service_group = Path(root).parent.stem
                compose_path = Path(root) / "docker-compose.yml"
                compose_files[service_group].append(compose_path)
                logger.debug(f"Found {compose_path}")
    return compose_files


COMPOSE_FILES = _find_compose_files()


def remove_partial_containers() -> None:
    logger.debug("Removing any partially running containers...")
    # reverse ordering here to remove core services last
    for group in reversed(SERVICE_GROUPS):
        compose_files = COMPOSE_FILES.get(group, [])
        for file in compose_files:
            run_command(f"docker compose -f {file} down --remove-orphans", check=False)


def launch_containers() -> None:
    logger.debug("Launching containers...")
    for group in SERVICE_GROUPS:
        compose_files = COMPOSE_FILES.get(group, [])
        for file in compose_files:
            service = file.parent.stem
            logger.debug(f"Launching {service}...")
            run_command(f"docker compose -f {file} up -d", check=False)
            if service == "postgres":
                logger.debug("Performing health check on database...")
                while True:
                    pg_check = run_command("docker exec playground-postgres pg_isready -U chap_admin", check=False)
                    if pg_check.returncode == 0:
                        logger.info("Postgres healthy")
                        break
                    logger.info("...")
                    time.sleep(2)
    logger.info("Containers launched successfully")


def main() -> None:
    logger.debug("Starting playground restoration script...")
    print("==========================================================")
    print("           PLAYGROUND MONOREPO RESTORATION START          ")
    print("==========================================================")
    check_env_files()
    create_docker_network()
    remove_partial_containers()
    launch_containers()
    print("==========================================================")
    print("         PLAYGROUND MONOREPO RESTORATION COMPLETE         ")
    print("==========================================================")


if __name__ == "__main__":
    main()

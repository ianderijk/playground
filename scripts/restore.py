import os
import time
from utils import ROOT, SERVICE_GROUPS, logger, run_command, create_services

logger.debug("Starting playground restoration")

NETWORK_NAME = "playground-routing"


def check_env_files() -> None:
    logger.debug("Checking for env files...")
    envs_dir = ROOT / "environments"
    env_files = os.listdir(envs_dir)
    if sorted(env_files) != ["global.env", "secrets.env"]:
        logger.critical("Failed to find env files")
        os._exit(1)
    logger.info("Found env files")


def create_docker_network() -> None:
    logger.debug("Checking for docker network")
    network_check = run_command(f"docker network inspect {NETWORK_NAME}", check=False)
    if network_check.returncode == 1:
        logger.debug(f"No network found, creating {NETWORK_NAME}")
        run_command(f"docker network create {NETWORK_NAME}")
        logger.info("Network created")
        return
    logger.info("Network found")


SERVICES = create_services()


def remove_partial_containers() -> None:
    logger.debug("Removing any partially running containers")
    # reverse ordering here to remove core services last
    for group in reversed(SERVICE_GROUPS):
        services = SERVICES.get(group, [])
        for service in services:
            run_command(
                f"docker compose -f {service.compose} down --remove-orphans",
                check=False,
            )


def launch_containers() -> None:
    logger.debug("Launching containers")
    for group in SERVICE_GROUPS:
        compose_files = SERVICES.get(group, [])
        for service in compose_files:
            service_name = service.compose.parent.stem
            logger.debug(f"Launching {service_name}")
            if service.env is not None:
                run_command(
                    f"docker compose --env-file {service.env} -f {service.compose} up -d",
                    check=False,
                )
            else:
                run_command(f"docker compose -f {service.compose} up -d", check=False)
            if service == "postgres":
                logger.debug("Performing health check on database")
                while True:
                    pg_check = run_command(
                        "docker exec playground-postgres pg_isready -U chap_admin",
                        check=False,
                    )
                    if pg_check.returncode == 0:
                        logger.info("Postgres healthy")
                        break
                    logger.info("...")
                    time.sleep(2)
    logger.info("Containers launched successfully")


def restore_services() -> None:
    logger.debug("Starting playground restoration script")
    print("==========================================================")
    print("           PLAYGROUND MONOREPO RESTORATION START          ")
    print("==========================================================")
    print("Checking for env files...")
    check_env_files()
    print("Creating docker network...")
    create_docker_network()
    print("Purging partial containers...")
    remove_partial_containers()
    print("Launching containers...")
    launch_containers()
    print("==========================================================")
    print("         PLAYGROUND MONOREPO RESTORATION COMPLETE         ")
    print("==========================================================")
    logger.info("Playground restored")

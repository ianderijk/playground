import os
from utils import SERVICE_GROUPS, logger, run_command, create_services

logger.debug("Starting playground restoration")

NETWORK_NAME = "playground-net"


def create_docker_network() -> None:
    logger.debug("Removing docker network")
    run_command(f"docker network rm {NETWORK_NAME}", check=False)
    logger.debug("Creating docker network")
    run_command(f"docker network create {NETWORK_NAME}", check=False)


SERVICES = create_services()


def remove_partial_containers() -> None:
    logger.debug("Removing any partially running containers")
    # reverse ordering here to remove core services last
    for group in reversed(SERVICE_GROUPS):
        services = SERVICES.get(group, [])
        for service in services:
            # os.chdir(service.dir)
            run_command(f"docker compose -f {service.compose} down --remove-orphans")


def launch_containers() -> None:
    logger.debug("Launching containers")
    for group in SERVICE_GROUPS:
        compose_files = SERVICES.get(group, [])
        for service in compose_files:
            service_name = service.compose.parent.stem
            service_dir = service.compose.parent.resolve()
            # os.chdir(service_dir)
            logger.debug(f"Launching {service_name}")
            if service.env is not None:
                run_command(
                    f"docker compose --env-file {service.env} -f {service.compose} up -d"
                )
            else:
                run_command(f"docker compose -f {service.compose} up -d")
    logger.info("Containers launched successfully")


def restore_services() -> None:
    logger.debug("Starting playground restoration script")
    print("==========================================================")
    print("           PLAYGROUND MONOREPO RESTORATION START          ")
    print("==========================================================")
    print("Purging partial containers...")
    remove_partial_containers()
    print("Creating docker network...")
    create_docker_network()
    print("Launching containers...")
    launch_containers()
    print("==========================================================")
    print("         PLAYGROUND MONOREPO RESTORATION COMPLETE         ")
    print("==========================================================")
    logger.info("Playground restored")

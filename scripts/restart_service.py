import os
from utils import ROOT, SERVICE_MAPPING, run_command, logger


def restart_service(service: str) -> None:
    parent_dir = next(x for x, y in SERVICE_MAPPING.items() if service in y)
    compose_path = ROOT / parent_dir / service
    env_file = ROOT / parent_dir / service / ".env"
    logger.debug(f"Removing container: {service}")
    os.chdir(compose_path)
    run_command("docker compose down --remove-orphans")
    logger.debug(f"Launching container: {service}")
    if env_file.exists():
        run_command(f"docker compose --env-file {env_file} up -d", check=False)
    else:
        run_command("docker compose up -d", check=False)
    logger.info(f"{service} restarted")

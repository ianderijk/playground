from utils import ROOT, run_command, logger


def restart_service(service: str) -> None:
    service_mapping = {
        "core": ("postgres", "pypi", "vault"),
        "storage": ("minio"),
        "apps": ("chapflix", "chaps_chores"),
        "apis": ("chapflix_api", "chaps_chores_api"),
    }
    parent_dir = next(x for x, y in service_mapping.items() if service in y)
    compose_path = ROOT / parent_dir / service / "docker-compose.yml"
    env_file =  ROOT / parent_dir / service / ".env"
    logger.debug(f"Removing container: {service}")
    if env_file.exists():
        run_command(f"docker compose --env-file {env_file} -f {compose_path} down --remove-orphans", check=False)
    else:
        run_command(f"docker compose -f {compose_path} down --remove-orphans", check=False)
    logger.debug(f"Launching container: {service}")
    run_command(f"docker compose -f {compose_path} up -d", check=False)
    logger.info(f"{service} restarted")

import typer
import os
from pathlib import Path
from restore import restore_services
from restart_service import restart_service
from utils import ROOT

SERVICES = [
    "chapflix_api",
    "chaps_chores_api",
    "chapflix",
    "chaps_chores",
    "postgres",
    "pypi",
    "vault",
    "minio",
]

app = typer.Typer(help="Playground management CLI")


def get_env_file() -> Path:
    env_path = ROOT / ".env"
    if not env_path.exists():
        typer.echo("Root .env file not found")
        os._exit(1)
    return env_path


@app.command()
def restore():
    typer.echo("Starting playground restoration...")
    restore_services()


@app.command()
def restart(service: str):
    typer.echo(f"Restarting {service}...")
    restart_service(service)
    typer.echo(f"{service} restarted")


if __name__ == "__main__":
    app()

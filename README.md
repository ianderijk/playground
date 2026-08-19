# Playground

This mono-repo houses infrastructure, deployment configs and data persitence for various self-hosted personal apps and their dependencies. Everything is managed using Docker Compose and orchestrated with a python CLI automating setup, teardown and disaster recovery.

## Contents

### Orchestration & CLI

Interactions with the orchestration automation are handled via the CLI. The intended entry point for accessing the CLI by adding a wrapper function to either `~/.bashrc` or `~/.zshrc`.

```
playground() {
    local REPO_DIR="/path/to/repo"
    "$REPO_DIR/.venv/bin/python" "$REPO_DIR/scripts/cli.py" "$@"
}
```

Using this function means interactions with the automation scripts is as below.

- Start/restart a service: `playground restart pypi`
- Stop a service: `playground stop chapflix`
- Stop all services: `playground stop-all`
- Full recovery: `playground restore`

### Core

#### Postgres

Backend database for various apps

- Version: 16
- Volume: `/media/ianderijk/Backup/postgres-data`
- Ports: 6543

#### PyPi

Local pypi index for hosting personal tooling

- Version: latest
- Volume: `/home/idr/packages:/data/packages`
- Ports: 8080

### Storage

#### Minio

s3 compatible object store

- Version: latest
- Volume: internal
- Ports: 9000:9001

### Apps

#### Chapflix

Local media streaming app for watching cartoons on weekends

- Version: 2.1.0
- Volume: `home/ianderijk/Backup/Chapflix2/content`
- Ports: 8042

### APIs

#### Chapflix-API

API used in Chapflix backend
- Version 1.0.0
- Volume: N/A
- Ports 8043

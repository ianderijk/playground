# Playground

This repo contains the various docker compose files for the apps I have built for my own use as well as the services they depend on. Everything in this repo is purely for personal pleasure and development.

## Contents

### Scripts

Scripts included in this directory have been written to facilitate recovery routines for either the entire suite of services or a given service. Interaction with these scripts is done via the CLI that is included in this directory and it is advised to add the below function to your .bashrc/.zshrc file.

```
playground() {
    local REPO_DIR="/path/to/repo"

    "$REPO_DIR/.venv/bin/python" "$REPO_DIR/scripts/cli.py" "$@"
}
```

Using this function means interactions with the automation scripts is as below.

`playground restart pypi`
`playground restore`
`playground stop chapflix`

### Core

#### Postgres

Backend database for various apps

Version: 16
Volume: `/media/ianderijk/Backup/postgres-data`
Ports: 6543

#### PyPi

Local pypi index for hosting personal tooling

Version: latest
Volume: `/home/idr/packages:/data/packages`
Ports: 8080

### Storage

#### Minio

Object store 


### Apps

#### Chapflix

Local media streaming app for watching cartoons on weekends

Version: 1.0.2
Volume: `home/ianderijk/Backup/Chapflix2/content`
Ports: 8042

#### Chaps Chores

Web app for tracking chores around the house
Version: 0.9.0
Volume: N/A
Ports: 8052

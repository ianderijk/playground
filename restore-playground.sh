#!/usr/bin/env bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NOCOLOUR='\033[0m'

log_info() {echo -e "${GREEN}[INFO]${NOCOLOUR} $1";}
log_warn() {echo -e "${YELLOW}[INFO]${NOCOLOUR} $1";}
log_error() {echo -e "${RED}[INFO]${NOCOLOUR} $1";}

echo "=========================================================="
echo "        PLAYGROUND MONOREPO RESURRECTION SCRIPT           "
echo "=========================================================="

if [ ! -f "environments/global.env" ] || [ ! -f "environments/secrets.env" ]; then
    log_error "Environment files are missing from environments/"
    log_error "Restore .env files before proceeding"
    exit 1
fi

log_info "Ensuring external docker network 'playground-routing' exists..."
docker network inspect playground-routing >/dev/null 2>&1 || \
    docker network create playground-routing

log_warn "Stopping any partially running containers..."
docker compose -f core/postgres/docker-compose.yml down --remove-orphans 2>/dev/null || true
# Either add other services here or write a for loop?

log_info "Launching core infrastructure..."
docker compose -f core/postgres/docker-compose.yml up -d

log_info "Waiting for database to become healthy..."
until docker exec homelab-postgres pg_isready -U chap_admin >/dev/null 2>&1; do
    echo -n "..."
    sleep 2
done
echo ""
log_info "Database is live and healthy!"

log_info "Launching apps..."
docker compose -f apps/chapflix/docker-compose.yml up -d
docker compose -f apps/chaps_chores/docker-compose.yml up -d

echo "=========================================================="
log_info "Restoration complete, all services are online."
echo "=========================================================="

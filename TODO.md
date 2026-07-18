root/
  .env
  .gitignore
  Makefile
  environments/
    - global.env
    - secrets.env
  core/
    postgres/
      - docker-compose.yml
    vault/
      - docker-compose.yml
    pypi/
      - docker-compose.yml
  apps/
    chapflix/
      - docker-compose.yml
  apis/
    chapflix-api/
      - docker-compose.yml
  storage/
    minio/
      - docker-compose.yml
    
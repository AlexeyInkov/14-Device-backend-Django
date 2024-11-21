#!/bin/bash
# takes two paramters, the domain name and the email to be associated with the certificate
#DOMAIN_URL=$1
#DOMAIN_EMAIL=$2
#
#echo MARIADB_USER=matomo > .env
#echo POSTGRES_DB_USER_PASSWORD=`openssl rand 30 | base64 -w 0` >> .env
##echo MARIADB_ROOT_PASSWORD=`openssl rand 30 | base64 -w 0` >> .env
#echo DOMAIN=${DOMAIN} >> .env
#echo EMAIL=${DOMAIN_EMAIL} >> .env

# Phase 1
docker compose -f ./docker-compose-initiate.yml up -d nginx
docker compose -f ./docker-compose-initiate.yml up certbot
docker compose -f ./docker-compose-initiate.yml down

# some configurations for let's encrypt
curl -L --create-dirs -o etc/letsencrypt/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
openssl dhparam -out etc/letsencrypt/ssl-dhparams.pem 2048

# Phase 2
crontab ./etc/crontab
docker compose -f ./docker-compose.yml up
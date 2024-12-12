#!/bin/bash
project_domain=inkov.online

sudo certbot --nginx -d $project_domain
sudo certbot --nginx -d dev-test.$project_domain

#!/bin/bash

sudo service gunicorn stop
sudo service gunicorn.socket stop

sudo rm -fr /etc/systemd/system/gunicorn.service
sudo rm -fr /etc/systemd/system/gunicorn.socket

sudo service nginx stop
sudo rm -fr /etc/nginx/sites-enabled/site_dc.conf

sudo systemctl start nginx
sudo systemctl enable nginx
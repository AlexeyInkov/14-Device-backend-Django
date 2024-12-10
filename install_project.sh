#!/bin/bash
base_python_interpreter=/home/www/.python/bin/python3.11
project_domain=inkov.online
project_path=`pwd`

#read -p "Python interpreter: " base_python_interpreter
#read -p "Your domain without protocol (for example, google.com): " project_domain

sudo certbot --nginx -d $project_domain

`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt

sed -i "s~dbms_template_path~$project_path~g" $project_path/etc/nginx/site_dc.conf $project_path/etc/systemd/gunicorn_dc.service
sed -i "s~dbms_template_domain~$project_domain~g" $project_path/etc/nginx/site_dc.conf $project_path/core/config/settings.py

sudo ln -s $project_path/etc/nginx/site_dc.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/etc/systemd/gunicorn_dc.service /etc/systemd/system/
sudo ln -s $project_path/etc/systemd/gunicorn_dc.socket /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start gunicorn_dc
sudo systemctl enable gunicorn_dc
sudo service nginx restart
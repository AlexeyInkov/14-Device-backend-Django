#!/bin/bash
base_python_interpreter=/home/www/.python/bin/python3.11
project_domain=inkov.online
project_path=`pwd`


`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
python -V

sed -i "s~dbms_template_path~$project_path~g" etc/nginx/site_dc.conf etc/systemd/gunicorn.service
sed -i "s~dbms_template_domain~$project_domain~g" etc/nginx/site_dc.conf core/config/settings.py

python core/manage.py migrate
python core/manage.py collectstatic

sudo ln -s $project_path/etc/nginx/site_dc.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/etc/systemd/gunicorn.service /etc/systemd/system/
sudo ln -s $project_path/etc/systemd/gunicorn.socket /etc/systemd/system/


sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo service nginx reload
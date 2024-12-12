#!/bin/bash
base_python_interpreter=/home/www/.python/bin/python3.11
project_domain=dev-test.inkov.online
project_path=`pwd`


`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
python -V

sed -i "s~dbms_template_path~$project_path~g" etc/nginx/dev-test_dc.conf etc/systemd/dev-test.service
sed -i "s~dbms_template_domain~$project_domain~g" etc/nginx/dev-test_dc.conf core/config/settings.py

python core/manage.py migrate
python core/manage.py collectstatic

sudo ln -s $project_path/etc/nginx/dev-test_dc.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/etc/systemd/dev-test.service /etc/systemd/system/
sudo ln -s $project_path/etc/systemd/dev-test.socket /etc/systemd/system/


sudo systemctl daemon-reload
sudo systemctl enable dev-test
sudo systemctl start dev-test
sudo service nginx reload
sudo systemctl daemon-reload
sudo systemctl restart dev-test
#!/bin/bash
base_python_interpreter=/home/www/.python/bin/python3.11
project_domain=inkov.online
gunicorn_name=dc
project_path=`pwd`

sudo apt update && sudo apt upgrade -y
sudo apt install certbot python3-certbot-nginx

echo -n "Удаляем настройки nginx? : "
read choice
if [choice=="y"]; then
  echo "Удаляем настройки nginx"
  sudo rm -r /etc/nginx/sites-enabled/*
fi
echo "Добавляем переадресацию 80 -> 443 в настройки nginx"
echo "server { listen 80; return 301 https://$host$request_uri; }" > /etc/nginx/sites-enabled/default

echo "restart nginx"
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "Проверяем certificates."
if [ ! -d "/etc/letsencrypt/live/$project_domain" ]; then
  echo "certificate does not exist."
  sudo certbot --nginx -d $project_domain
fi

echo "Устанавливаем окружение и зависимости."
`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
python -V

echo "Подготовка настроек Nginx и Gunicorn"
sed -i "s~dbms_template_path~$project_path~g" etc/nginx/my_site.conf etc/systemd/gunicorn.service
sed -i "s~dbms_template_domain~$project_domain~g" etc/nginx/my_site.conf core/config/settings.py etc/systemd/gunicorn.service etc/systemd/gunicorn.socket

echo "migrate and static"
python core/manage.py migrate
python core/manage.py collectstatic -y

echo "Копирование настроек Nginx и Gunicorn"
sudo cp -f etc/nginx/my_site.conf etc/nginx/$project_domain.conf
sudo cp -f etc/systemd/gunicorn.service etc/systemd/$project_domain.service
sudo cp -f etc/systemd/gunicorn.socket etc/systemd/$project_domain.socket

echo "Подключение настроек Nginx и Gunicorn"
sudo ln -s $project_path/etc/nginx/$project_domain.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/etc/systemd/$project_domain.service /etc/systemd/system/
sudo ln -s $project_path/etc/systemd/$project_domain.socket /etc/systemd/system/

echo "Перезагрузка Nginx и Gunicorn"
sudo systemctl daemon-reload
sudo systemctl enable $project_domain
sudo systemctl start $project_domain
sudo service nginx reload
sudosudo systemctl restart $project_domain
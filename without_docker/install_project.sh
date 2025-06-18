#!/bin/bash
base_python_interpreter=/home/www/.python/bin/python3.11
project_domain=device-control.site
project_path=`pwd`

sudo apt update && sudo apt upgrade -y
sudo apt install certbot python3-certbot-nginx

echo -n "Удаляем настройки nginx? y/n : "
read choice
yes="y"
if [ $choice = $yes ]; then
  echo "Удаляем настройки nginx"
  sudo rm -r /etc/nginx/sites-enabled/*
fi
echo "Добавляем переадресацию 80 -> 443 в настройки nginx"
sudo ln -s $project_path/etc/nginx/default /etc/nginx/sites-enabled/

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

echo "migrate and static"
python core/manage.py migrate
python core/manage.py collectstatic

echo "Остановка Gunicorn"
systemctl stop gunicorn_$project_domain
systemctl stop gunicorn_$project_domain.socket

echo "Остановка Celery"
systemctl stop celery_$project_domain
systemctl stop celery_beat_$project_domain

echo "Удаление Gunicorn"
sudo rm -r /etc/systemd/system/gunicorn_$project_domain.service
sudo rm -r /etc/systemd/system/gunicorn_$project_domain.socket

echo "Удаление Celery"
sudo rm -r /etc/systemd/system/celery_$project_domain.service
sudo rm -r /etc/systemd/system/celery_beat_$project_domain.service

echo "Копирование настроек Nginx"
sudo cp -f etc/nginx/my_site.conf /etc/nginx/sites-available/$project_domain.conf

echo "Копирование настроек Gunicorn"
sudo cp -f etc/systemd/gunicorn.service /etc/systemd/system/gunicorn_$project_domain.service
sudo cp -f etc/systemd/gunicorn.socket /etc/systemd/system/gunicorn_$project_domain.socket

echo "Копирование настроек Celery"
sudo cp -f etc/celery/celery /etc/conf.d/celery
sudo cp -f etc/systemd/celery.service /etc/systemd/system/celery_$project_domain.service
sudo cp -f etc/systemd/celerybeat.service /etc/systemd/system/celery_beat_$project_domain.service

echo "Подготовка настроек Nginx, Gunicorn и Celery"
sudo sed -i "s~dbms_template_path~$project_path~g" /etc/nginx/sites-available/$project_domain.conf /etc/systemd/system/gunicorn_$project_domain.service /etc/systemd/system/celery_$project_domain.service /etc/systemd/system/celery_beat_$project_domain.service /etc/conf.d/celery
sudo sed -i "s~dbms_template_domain~$project_domain~g" /etc/nginx/sites-available/$project_domain.conf /etc/systemd/system/gunicorn_$project_domain.service /etc/systemd/system/gunicorn_$project_domain.socket

echo "Подключение настроек Nginx"
sudo ln -s /etc/nginx/sites-available/$project_domain.conf /etc/nginx/sites-enabled/

echo "Перезагрузка"
sudo systemctl daemon-reload

echo "Запуск Gunicorn"
sudo systemctl enable gunicorn_$project_domain.socket
sudo systemctl start gunicorn_$project_domain.socket
sudo systemctl restart gunicorn_$project_domain

echo "Запуск Celery"
sudo systemctl enable celery_$project_domain
sudo systemctl start celery_$project_domain
sudo systemctl restart celery_$project_domain

echo "Запуск Celery Beat"
sudo systemctl enable celery_beat_$project_domain
sudo systemctl start celery_beat_$project_domain
sudo systemctl restart celery_beat_$project_domain

sudo service nginx reload
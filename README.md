
### Клонируем репозиторий
```
git clone https://gitlab.com/device_control/backend-django.git
cd backend-django
chmod +x install_project.sh
mv .env_template .env
```
### Настраиваем переменные
```
nano .env
```
### в install_project.sh
##### base_python_interpreter=/home/www/.python/bin/python3.11
##### project_domain=example.com

### Install project (nginx, sertbot, gunicorn)
```
./install_project.sh
```

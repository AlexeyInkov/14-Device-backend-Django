
### Клонируем репозиторий
```
git clone https://github.com/AlexeyInkov/14-Device-backend-Django.git
```
### Переименовываем директорию
```
mv 14-Device-backend-Django new_dir_name
```
### Подготовка к настройке
```
cd new_dir_name
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

### Создание директории для настроек Celery
```sudo mkdir /etc/conf.d```

### Install project (nginx, sertbot, gunicorn)
```
./install_project.sh
```

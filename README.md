
### Клонируем репозиторий
```
git clone https://github.com/AlexeyInkov/14-Device-backend-Django.git
cd core
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

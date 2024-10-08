
- копируем чистую базу с админом

```python manage.py loaddata fixtures/clean_admin.json```

- копируем приборы на 19/09/2024

```python manage.py loaddata fixtures/db_20240918_new_address_region.json```

- сохранить базу

```python manage.py dumpdata --indent 4 > fixtures/db_20240918_new_address_region.json```

-изменить encoding на utf-8

new db
python manage.py migrate

python manage.py loaddata fixtures/clean_with_superuser.json
or
python manage.py createsuperuser
python manage.py dumpdata --indent 4 > fixtures/clean_with_superuser.json

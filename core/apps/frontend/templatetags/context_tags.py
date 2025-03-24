from django import template
from django.db.models import QuerySet

from config.settings import (
    HEADERS_ADDRESS,
    HEADERS_DEVICE,
    HEADERS_VERIFICATION,
    HEADERS_VERIFICATION_UPDATE,
)

register = template.Library()


@register.simple_tag(name="get_headers_address")
def get_headers_address() -> dict:
    return HEADERS_ADDRESS


@register.simple_tag(name="get_headers_device")
def get_headers_device() -> dict:
    return HEADERS_DEVICE


@register.simple_tag(name="get_headers_verification")
def get_headers_verification() -> dict:
    return HEADERS_VERIFICATION


@register.simple_tag(name="get_headers_verification_update")
def get_headers_verification_update() -> dict:
    return HEADERS_VERIFICATION_UPDATE


@register.filter
def dictitem(dictionary: dict, key: str) -> str:
    return dictionary.get(key)


@register.filter
def attr(obj, name):
    # возвращает значение атрибута по имени поля
    value = getattr(obj, name, None)
    # print(f"{name} : {value}")
    if value is not None:
        return value
    return "пусто"


@register.filter()
def get_instance_from_query_pk(query: QuerySet, pk: str):
    # возвращает экземпляр из QuerySet по pk
    return query.get(pk=int(pk))


@register.filter
def convert_date_str(date_field: str) -> str:
    # Конвертирует YYYY-MM-DD HH:mm:ss.ms -> DD.MM.YYYY
    if date_field is not None:
        date_field = "2024-12-25 21:13:06.006498"
        return ".".join(date_field.split()[0].split("-")[-1::-1])
    return "пусто"

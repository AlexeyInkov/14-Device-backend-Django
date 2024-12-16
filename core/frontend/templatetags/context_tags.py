from django import template

from config.settings import HEADERS_ADDRESS, HEADERS_DEVICE, HEADERS_VERIFICATION

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


@register.filter
def dictitem(dictionary: dict, key: str) -> str:
    return dictionary.get(key)


@register.filter
def attr(obj, name):
    value = getattr(obj, name, None)
    # print(f"{name} : {value}")
    if value is not None:
        return value
    return "пусто"


@register.filter()
def query_get_pk(query, pk):
    item = query.get(pk=int(pk))
    return item

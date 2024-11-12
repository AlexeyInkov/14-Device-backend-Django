from django import template

from config.settings import HEADERS_ADDRESS, HEADERS_DEVICE

register = template.Library()


@register.simple_tag(name="get_headers_address")
def get_headers_address() -> dict:
    return HEADERS_ADDRESS


@register.simple_tag(name="get_headers_device")
def get_headers_device() -> dict:
    return HEADERS_DEVICE


@register.filter
def dictitem(dictionary: dict, key: str) -> str:
    return dictionary.get(key)


@register.filter
def attr(obj, name):
    return getattr(obj, name, None)

from time import sleep

from requests import Response, request

from django.conf import settings


def request_to_arshin(reg_number: str, number: str) -> Response:
    url = f"https://fgis.gost.ru/fundmetrology/cm/xcdb/vri/select?fq=mi.mitnumber:{reg_number}*&fq=mi.number:{number}&q=*&fl=org_title,mi.mitnumber,mi.mititle,mi.mitype,mi.modification,mi.number,verification_date,valid_date&sort=verification_date+desc,org_title+asc&rows=200&start=0"
    sleep(settings.TIME_DDOS_FOR_REQUEST)
    response = request("get", url)
    return response

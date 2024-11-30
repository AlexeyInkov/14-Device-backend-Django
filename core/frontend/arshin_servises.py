from time import sleep

from requests import Session, Response, request


def request_to_arshin(reg_number: str, number: str) -> Response:
    url = f"https://fgis.gost.ru/fundmetrology/cm/xcdb/vri/select?fq=mi.mitnumber:{reg_number}*&fq=mi.number:{number}&q=*&fl=org_title,mi.mitnumber,mi.mititle,mi.mitype,mi.modification,mi.number,verification_date,valid_date&sort=verification_date+desc,org_title+asc&rows=200&start=0"
    sleep(2)
    response = request('get', url, timeout=2)
    # my_logger.info(f"({url}) - {response.status_code}")
    print(response.text)
    return response

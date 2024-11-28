from requests import Session, Response


def request_to_arshin(session: Session, reg_number: str, number: str) -> Response:
    url = f"https://fgis.gost.ru/fundmetrology/cm/xcdb/vri/select?fq=mi.mitnumber:{reg_number}*&fq=mi.number:{number}&q=*&fl=org_title,mi.mitnumber,mi.mititle,mi.mitype,mi.modification,mi.number,verification_date,valid_date&sort=verification_date+desc,org_title+asc&rows=200&start=0"
    response = session.get(url, timeout=2)
    # my_logger.info(f"({url}) - {response.status_code}")
    return response

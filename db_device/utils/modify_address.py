"""Модификация адреса и региона при импорте из файла"""

from db_device.wsgi import *
from metering_unit.models import Address, Region, TypeStreet, Street


def change_street(address, street, tp):
    print(tp, street)
    if Street.objects.filter(name=street).exists():
        address.street_new = Street.objects.filter(name=street).first()
        address.street = ""
        print("Existing", address.street_new)
    else:
        new_street = Street.objects.create(
            name=street, type_street=TypeStreet.objects.get(name=tp)
        )
        address.street_new = new_street
        address.street = ""
        print("NEW", address.street_new)
    address.save()


def change_city(address):
    curr = address.street.split(",")
    print(curr[0])
    if Region.objects.filter(name=curr[0]).exists():
        address.region = Region.objects.filter(name=curr[0]).first()
        curr.pop(0)
    else:
        new = Region.objects.create(name=curr[0])
        new.save()
        address.region = new
        curr.pop(0)
    address.street = ",".join(map(lambda st: st.strip(), curr))
    address.save()


queryset = Address.objects.all()
for address in queryset:
    # города спб, стрельна, ломоносов, петродворец, сестрорецк, зеленогорск переносит в регион
    if address.street:
        curr = address.street.split(",")
        if (
            curr[0].lower().find("спб") != -1
            or curr[0].lower().find("стрельна") != -1
            or curr[0].lower().find("ломоносов") != -1
            or curr[0].lower().find("петродворец") != -1
            or curr[0].lower().find("сестрорецк") != -1
            or curr[0].lower().find("зеленогорск") != -1
            or curr[0].lower().find("колпино") != -1
        ):
            # input(f"хочу изменить {curr[0]} y/n")
            change_city(address)
        else:
            print("пропустил", curr[0])
    # в пустой регион ставит СПб
    if address.region is None:
        print(f"подставляет СПб в {address.street}")
        address.region = Region.objects.filter(name="СПб").first()
        address.save()

    # Отделяем тип от названия
    if address.street:
        curr = address.street.split()
        print(curr)
        for index, elem in enumerate(curr):
            if elem in ["наб", "наб."]:
                curr.pop(index)
                change_street(
                    address, " ".join(map(lambda st: st.strip(), curr)), "наб."
                )
                break
            elif elem == "бул.":
                curr.pop(index)
                change_street(
                    address, " ".join(map(lambda st: st.strip(), curr)), "бул."
                )
                break
            elif elem in ["ш.", "ш", "шоссе"]:
                curr.pop(index)
                change_street(address, " ".join(map(lambda st: st.strip(), curr)), "ш.")
                break
            elif elem == "пер.":
                curr.pop(index)
                change_street(
                    address, " ".join(map(lambda st: st.strip(), curr)), "пер."
                )
                break
            elif elem in ["пр.", "пр"]:
                curr.pop(index)
                change_street(
                    address, " ".join(map(lambda st: st.strip(), curr)), "пр."
                )
                break
            elif elem in ["ул.", "ул,", "Ул"]:
                print(address.street)
                curr.pop(index)
                change_street(
                    address, " ".join(map(lambda st: st.strip(), curr)), "ул."
                )
                break
        else:
            print("нет совпадений")
            change_street(address, address.street, "ул.")

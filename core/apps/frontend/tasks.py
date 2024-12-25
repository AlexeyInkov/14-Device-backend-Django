import csv

from celery import shared_task
from celery_singleton import Singleton

from apps.device.models import (
    Organization,
    UserToOrganization,
    Region,
    TypeStreet,
    Street,
    Address,
    MeteringUnit,
    DeviceInstallationPoint,
    TypeToRegistry,
    Device,
    DeviceVerification
)
from apps.frontend.servises.arshin_servises import request_to_arshin
from apps.frontend.servises.db_services import save_verification


# @shared_task(base=Singleton, name='tasks.get_device_verifications')
# def get_device_verifications(device_id: int) -> str:
#     print("run get_device_verifications")
#     device = Device.objects.get(id=device_id)
#     if device:
#         for reg_number in device.type_of_file.numbers_registry.split(","):
#             response = request_to_arshin(reg_number, device.factory_number)
#             if response.status_code == 200:
#                 response = response.json()["response"]
#                 if response['numFound'] > 0:
#                     verifications = response["docs"]
#                     if verifications:
#                         for verification in verifications:
#                             save_verification(device_id, verification)
#         return "Done"
#     return "Device not found"


@shared_task(base=Singleton, name='tasks.refresh_all_valid_date')
def refresh_valid_date() -> str:
    print("run refresh_valid_date")
    devices = Device.objects.all().order_by("updated_at").only("id")
    for index, device in enumerate(devices):
        print("index=", index)
        # get_device_verifications.delay(device.pk)
        print("run get_device_verifications")
        for reg_number in device.type_of_file.numbers_registry.split(","):
            response = request_to_arshin(reg_number, device.factory_number)
            if response.status_code == 200:
                response = response.json()["response"]
                if response['numFound'] > 0:
                    verifications = response["docs"]
                    if verifications:
                        for verification in verifications:
                            save_verification(device.id, verification)
    return "Done"


def get_or_create_instance(model, data: dict):
    instance = model.objects.filter(**data)
    if len(instance) > 1:
        raise Exception("Duplicate instance")
    elif not instance:
        instance = model.objects.create(**data)
    return instance.id


@shared_task(name='tasks.download_device_from_file_into_db')
def download_file_to_db(filename: str, user_id: str):
    error_filename = "".join((filename[:-4], "_error", filename[-4:]))
    with open(filename, "r", encoding='cp1251') as file:
        reader = csv.DictReader(file, delimiter=";")
        with open(error_filename, "w", encoding='cp1251', newline='') as csv_file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            try:
                if reader.fieldnames != ['Наименование абонента', 'Город', 'Наименование улицы', 'Тип улицы', '№ дома', 'Корп', 'Лит', 'ТЦ', 'Труба', 'Тип', 'Ду', 'Номер', 'Дата', 'МПИ', 'ТСО', '№ Тотэм']:
                    raise ValueError
            except ValueError:
                print("Поля не соответствуют")
            else:

                count_error = 0
                for row in reader:
                    try:
                        customer = {
                            "name": row["Наименование абонента"].strip(),
                        }
                        customer_id = get_or_create_instance(Organization, data=customer)

                        user_to_organization = {'user': user_id, 'organization': customer_id}
                        get_or_create_instance(UserToOrganization, data=user_to_organization)

                        tso = {"name": row["ТСО"].strip()}
                        tso_id = get_or_create_instance(Organization, data=tso)

                        user_to_organization = {'user': user_id, 'organization': tso_id}
                        get_or_create_instance(UserToOrganization, data=user_to_organization)

                        region = {"name": row["Город"].strip()}
                        region_id = get_or_create_instance(Region, data=region)

                        type_street = {"name": row['Тип улицы'].strip()}
                        if not type_street:
                            type_street = " "
                            print("-------------------------------Васька---------------------------")
                        type_street_id = get_or_create_instance(TypeStreet, data=type_street)

                        street = {"name": row["Наименование улицы"].strip()}
                        if type_street_id:
                            street.update({"type_street": type_street_id})
                        street_id = get_or_create_instance(Street, data=street)

                        address = {
                            "region": region_id,
                            "street": street_id,
                            "house_number": row["№ дома"].strip(),
                            "corp": row["Корп"].strip(),
                            "liter": row["Лит"].strip(),

                        }
                        address_id = get_or_create_instance(Address, data=address)

                        metering_unit = {
                            'customer': customer_id,
                            'tso': tso_id,
                            'address': address_id,
                            'itp': row["ТЦ"].strip(),
                            'totem_number': row["№ Тотэм"].strip(),
                        }
                        metering_unit_id = get_or_create_instance(MeteringUnit, data=metering_unit)

                        installation_point = {'name': row["Труба"].strip()}
                        installation_point_id = get_or_create_instance(DeviceInstallationPoint, data=installation_point)

                        type_of_file = {'device_type_file': row["Тип"].strip()}
                        type_of_file_id = get_or_create_instance(TypeToRegistry, data=type_of_file)

                        # mod = row["Ду"]
                        # mod_id = req_api('device/mod/', body=mod, headers=headers)['id']

                        device = {
                            'metering_unit': metering_unit_id,
                            'installation_point': installation_point_id,
                            'type_of_file': type_of_file_id,
                            'factory_number': row["Номер"].strip(),
                        }
                        device_id = get_or_create_instance(Device, data=device)

                        data = row["Дата"].strip()
                        if data:
                            data = data.split('.')

                            device_verification = {
                                'device': device_id,
                                'valid_date': '-'.join((data[2], data[1], data[0])),
                            }
                            print(device_verification)
                            get_or_create_instance(DeviceVerification, data=device_verification)
                    except BaseException as e:
                        print(e)
                        writer.writerow(row)
                        count_error += 1
                print(count_error)


# TODO новые tasks
def user_organization():
    pass


def device_field():
    pass

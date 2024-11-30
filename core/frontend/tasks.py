from time import sleep

from celery import shared_task

from device.models import Device
from frontend.arshin_servises import request_to_arshin
from frontend.db_services import save_verification


@shared_task(name='tasks.get_device_verifications')
def get_device_verifications(device_id):
    print("run get_device_verifications")
    device = Device.objects.get(id=device_id)
    print(device)
    # session = requests.Session()
    if device:
        print("numbers_registry=", device.type_of_file.numbers_registry.split(","))
        for reg_number in device.type_of_file.numbers_registry.split(","):
            print(reg_number, device.factory_number)

            response = request_to_arshin(
                reg_number, device.factory_number
            )

            response = response.json()["response"]
            if response['numFound'] > 0:
                verifications = response["docs"]
                print("verifications=", verifications)
                if verifications:
                    for verification in verifications:
                        print("verification=", verification)
                        save_verification(device_id, verification)



@shared_task(name='tasks.refresh_valid_date')
def refresh_valid_date():
    print("run refresh_valid_date")
    devices = Device.objects.all().order_by("updated_at").only("id")
    print("devices_id=", devices)
    for index, device in enumerate(devices):
        print("index=", index)
        get_device_verifications(device.pk)


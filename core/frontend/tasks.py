from celery import shared_task
from celery_singleton import Singleton
from device.models import Device
from frontend.arshin_servises import request_to_arshin
from frontend.db_services import save_verification


@shared_task(base=Singleton, name='tasks.get_device_verifications')
def get_device_verifications(device_id: int) -> str:
    print("run get_device_verifications")
    device = Device.objects.get(id=device_id)
    if device:
        for reg_number in device.type_of_file.numbers_registry.split(","):
            response = request_to_arshin(reg_number, device.factory_number)
            if response.status_code == 200:
                response = response.json()["response"]
                if response['numFound'] > 0:
                    verifications = response["docs"]
                    if verifications:
                        for verification in verifications:
                            save_verification(device_id, verification)
        return "Done"
    return "Device not found"


@shared_task(base=Singleton, name='tasks.refresh_valid_date')
def refresh_valid_date() -> str:
    print("run refresh_valid_date")
    devices = Device.objects.all().order_by("updated_at").only("id")
    # print("devices_id=", devices)
    for index, device in enumerate(devices):
        print("index=", index)
        get_device_verifications.delay(device.pk)
    return "Done"


# TODO новые tasks
def user_organization():
    pass


def device_field():
    pass
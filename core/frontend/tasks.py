import requests
from celery import shared_task
from celery.schedules import crontab

from config.celery import app
from device.models import Device
from frontend.arshin_servises import request_to_arshin
from frontend.db_services import save_verification


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        10.0, refresh_valid_date.s(), name="refresh_valid_date_every_10"
    )
    #
    # # Calls test('hello') every 30 seconds.
    # # It uses the same signature of previous task, an explicit name is
    # # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task(30.0, test.s("hello"), name="add every 30")
    #
    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s("world"), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(minute="10"),
        # crontab(hour=7, minute=30, day_of_week=1),
        refresh_valid_date.s(),
        name="refresh_valid_date_monday",
    )


@shared_task
def get_device_verifications(device_id):
    device = Device.objects.get(id=device_id)
    session = requests.Session()
    if device:
        for reg_number in device.type_of_file.numbers_registry:
            verifications = request_to_arshin(
                session, reg_number, device.factory_number
            ).json()["response"]["docs"]
            if verifications:
                for verification in verifications:
                    save_verification(device_id, verification)


@app.task
def refresh_valid_date():
    devices_id = Device.objects.all().only("id")
    for index, devices_id in enumerate(devices_id):
        print(index)
        get_device_verifications.delay(devices_id)

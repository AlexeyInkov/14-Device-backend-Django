# Generated by Django 5.1.4 on 2025-02-06 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0007_remove_device_si_name_typetoregistryimport_si_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="typetoregistryimport",
            name="si_name",
        ),
        migrations.AddField(
            model_name="typetoregistry",
            name="si_name",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="typetoreg",
                to="device.siname",
            ),
        ),
    ]

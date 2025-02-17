# Generated by Django 5.1.4 on 2025-02-06 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0005_remove_device_name_si_device_si_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="installationpoint",
            options={
                "ordering": ["order"],
                "verbose_name_plural": "installation_points",
            },
        ),
        migrations.AlterModelOptions(
            name="modification",
            options={"verbose_name_plural": "mods"},
        ),
        migrations.AlterModelOptions(
            name="registrynumber",
            options={"verbose_name_plural": "registry_numbers"},
        ),
        migrations.AlterModelOptions(
            name="typename",
            options={"verbose_name_plural": "types"},
        ),
        migrations.AlterModelOptions(
            name="verification",
            options={"verbose_name_plural": "verifications"},
        ),
        migrations.RemoveField(
            model_name="verification",
            name="is_delete",
        ),
        migrations.AddField(
            model_name="verification",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
    ]

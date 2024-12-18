# Generated by Django 5.1.4 on 2024-12-16 20:37

from django.db import migrations, models
from slugify import slugify


def create_organization_slug(apps, schema_editor):
    Organization = apps.get_model("metering_unit", 'Organization')
    for org in Organization.objects.all():
        # -----------------------------------
        # TODO удалить на новой fixture
        if org.pk == 61:
            if input("Есть проблемы с Organization.slug No/yes") == "yes":
                for uto in apps.get_model('metering_unit', 'UserToOrganization').objects.filter(organization=org):
                    uto.delete()
                org.delete()
        # -----------------------------------
        org.slug = slugify(org.name)
        org.save()


class Migration(migrations.Migration):

    dependencies = [
        ("metering_unit", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="slug",
            field=models.SlugField(default="", max_length=100),
        ),
        migrations.RunPython(create_organization_slug),
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]

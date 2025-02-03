from django.forms import ModelForm

from apps.device.models import TypeToRegistryImport


class TypeToRegistryImportForm(ModelForm):
    class Meta:
        model = TypeToRegistryImport
        fields = ("csv_file",)

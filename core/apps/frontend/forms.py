from django import forms
from django.forms import inlineformset_factory

from apps.device.models import Verification, Device


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class UploadFileForm(forms.Form):
    file_field = MultipleFileField()


class VerificationForm(forms.Form):
    class Meta:
        model = Verification
        fields = '__all__'
        widgets = {}


DeviceVerificationFormset = inlineformset_factory(
    Device,
    Verification,
    form=VerificationForm,
    extra=0,
    can_delete=False,
)

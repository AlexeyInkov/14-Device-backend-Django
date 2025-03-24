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


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        fields = (
            "org_title",
            "mit_number",
            "mit_notation",
            "mi_modification",
            "mi_number",
            "verification_date",
            "valid_date",
            "is_actual",
            "is_published",
        )
        exclude = ("id", "created_at", "updated_at", "device")
        widgets = {
            "org_title": forms.TextInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "mit_number": forms.TextInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "mit_notation": forms.TextInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "mi_modification": forms.TextInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "mi_number": forms.TextInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "verification_date": forms.DateInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "valid_date": forms.DateInput(
                attrs={"readonly": True, "class": "form-control", "style": {}}
            ),
            "is_actual": forms.CheckboxInput(
                attrs={"readonly": False, "class": "", "style": {}}
            ),
            "is_published": forms.CheckboxInput(
                attrs={"readonly": False, "class": "", "style": {}}
            ),
        }


# https://evileg.com/ru/post/455/
# https://www.squash.io/advanced-django-forms-dynamic-generation-formsets-and-custom-widgets/
DeviceVerificationFormset = inlineformset_factory(
    Device,
    Verification,
    form=VerificationForm,
    extra=0,
    can_delete=True,
)

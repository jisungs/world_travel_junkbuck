from django import forms
from .models import PhotoMetadata

class PhotoForm(forms.ModelForm):
    class Meta:
        models = PhotoMetadata
        fields = ['name','memo']
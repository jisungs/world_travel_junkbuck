from django import forms
from .models import PhotoMetadata, Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        models = PhotoMetadata
        fields = ['name','memo']

class TravelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['name' ,'image']
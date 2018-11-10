from django import forms
from django.forms import ModelForm
from app.models import Photo


class PictureForm(ModelForm):
    class Meta:
        model = Photo
        fields = ["picture"]
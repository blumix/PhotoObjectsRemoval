from django import forms
from django.forms import ModelForm
from app.models import Photo


class PictureForm(ModelForm):

    types = (
        ('Select_points', 'Select_points'),
        ('Draw_circles', 'Draw_circles'),
    )

    action_type = forms.ChoiceField(choices=types, help_text='Choose action type')

    class Meta:
        model = Photo
        fields = ["picture", "action_type"]
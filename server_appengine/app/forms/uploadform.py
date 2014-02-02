#coding: utf-8

from django import forms
from app.models.upload import UploadModel
class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel
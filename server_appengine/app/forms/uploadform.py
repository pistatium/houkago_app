#coding: utf-8
from google.appengine.api import images

from django import forms
from app.models.upload import UploadModel
class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadModel

    # resize max to 512 x 512
    def clean_file(self):
    	img = self.cleaned_data['file']

    	return {
    		"img" :images.resize(img.read(), 320, 320),
    		"content_type": img.content_type
    	}
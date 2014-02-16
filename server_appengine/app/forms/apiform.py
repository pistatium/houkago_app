#coding: utf-8
from django import forms
from app.libs.utils import make_api_key


# api form base 
class ApiForm(forms.Form):
    client  = forms.RegexField('^[A-Za-z0-9_]+$')
    key     = forms.CharField()
    version = forms.RegexField('^1$')

    def clean_key(self):
        client = self.cleaned_data['client']
        key = self.cleaned_data['key']
        calced_key = make_api_key(client)
        if key != calced_key:
            raise forms.ValidationError(u"invalid key")
        return key


class RecentAppForm(ApiForm):
    offset = forms.IntegerField(
            min_value = 0,
            max_value = 1000,
            initial = 0,
            required = False,
    )

    count  = forms.IntegerField(
            min_value = 1,
            max_value = 50,
            initial = 10,
            required = False,
    )
    platform = forms.IntegerField(required = True)

    def clean_platform(self):
        platform = self.cleaned_data['platform']
        if platform == 0:
            raise forms.ValidationError(u"invalid platform")
        return platform

class DetailAppForm(ApiForm):
    pass

# コールバック用バリデーションルール
class callbackform(forms.Form):
    callback = forms.RegexField('^[a-zA-Z0-9_-]{1,20}$')

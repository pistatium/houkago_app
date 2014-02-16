#coding: utf-8
from django import forms
from app.libs.utils import make_api_key

class UseApiForm(forms.Form):
    client_name  = forms.CharField(
        label = u"APIを使用するアプリ名",
    )
    description  = forms.CharField(
        label = u"アプリの詳細 (利用目的、URLなど)",
        max_length = 480, 
        required = True, 
        widget=forms.Textarea(attrs={"rows": 6,"cols":100, "maxlength":480})
    )


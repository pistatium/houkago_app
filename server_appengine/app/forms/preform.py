#coding: utf-8
from django import forms

class PreForm(forms.Form):
    user_mail = forms.EmailField(
        label = "メール",
        required = True,
    )
    user_mail.widget.attrs.update({'placeholder': 'e-mail'})
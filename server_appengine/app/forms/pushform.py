#coding: utf-8

from django import forms

# -- Rules of validation -------------------------------
# ------------------------------------------------------

from app.libs.arrays import platforms, show_status

# regist用バリデーションルール
class PushForm(forms.Form):
    best_1_app = forms.IntegerField(
        required = False,
    )
    best_2_app = forms.IntegerField(
        required = False,
    )
    best_3_app = forms.IntegerField(
        required = False,
    )
    platform = forms.ChoiceField(
        label   = u"プラットフォーム",
        choices = platforms, 
    )

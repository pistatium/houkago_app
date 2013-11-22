#coding: utf-8
from django import forms

# -- Rules of validation -------------------------------
# ------------------------------------------------------

# regist用バリデーションルール
class RegistForm(forms.Form):
    device_id    = forms.CharField(max_length = 50, required = True)
    device_hash  = forms.CharField(max_length = 50, required = True)
    
# regist用バリデーションルール
class makeThreadForm(forms.Form):
    device_id  = forms.CharField(max_length=50, required=True)
    token      = forms.CharField(max_length=50, required=True)
    title      = forms.CharField(max_length = 60, required = True)
    body       = forms.CharField(max_length = 2048, required = True)
    category   = forms.IntegerField(required = True)
    uname       = forms.CharField(max_length = 15, required = False, initial= None)

# regist用バリデーションルール
class makeResForm(forms.Form):
    device_id  = forms.CharField(max_length=50, required=True)
    token      = forms.CharField(max_length=50, required=True)
    uname     = forms.CharField(max_length = 15, required = False)
    body       = forms.CharField(max_length = 2048, required = True)
    thread_id  = forms.IntegerField(required = True)

#
class getThreadForm(forms.Form):
    count     = forms.IntegerField(initial=100)
    page      = forms.IntegerField(initial=0)
    status    = forms.IntegerField(initial=1)
    sortby    = forms.RegexField('^(created|updated|count|evaluated)?$')
    reverse   = forms.IntegerField(required = False)
    category  = forms.IntegerField(initial=0)

class getResForm(forms.Form):
    thread_id = forms.IntegerField()
    count     = forms.IntegerField(initial=100)
    page      = forms.IntegerField(initial=0)
    

# スレいいねAPI
class evaluateThreadForm(forms.Form):
    device_id  = forms.CharField(max_length=50, required=True)
    token      = forms.CharField(max_length=50, required=True)
    thread_id  = forms.IntegerField(required = True)
    is_plus    = forms.IntegerField()

# レスいいねAPI
class evaluateResForm(forms.Form):
    device_id  = forms.CharField(max_length=50, required=True)
    token      = forms.CharField(max_length=50, required=True)
    res_id  = forms.IntegerField(required = True)
    is_plus    = forms.IntegerField()
    
# レス削除API
class deleteResForm(forms.Form):
    device_id  = forms.CharField(max_length=50, required=True)
    token      = forms.CharField(max_length=50, required=True)
    res_id     = forms.IntegerField(required = True)
    del_key    = forms.RegexField('^delete_kamatte_0910$')
    
# スレッド削除API
class deleteThreadForm(forms.Form):
    device_id  = forms.CharField(max_length=50, required=True)
    token      = forms.CharField(max_length=50, required=True)
    thread_id     = forms.IntegerField(required = True)
    del_key    = forms.RegexField('^delete_kamatte_0910$')
    
# コールバック用バリデーションルール
class CallbackForm(forms.Form):
    callback = forms.RegexField('^[a-zA-Z0-9_-]{1,20}$')

#coding: utf-8

from django import forms
from app.models.developer import Developer
import re
# -- Rules of validation -------------------------------
# ------------------------------------------------------

# regist用バリデーションルール
class RegistForm(forms.Form):
    user_alias     = forms.CharField(
        label = u"ユーザーID(必須, 変更不可)",
        max_length = 15,
        required = True,
        initial = None,
    )
    uname       = forms.CharField(
        label = u"開発者名",
        max_length = 25,
        required = True,
        initial= None
    )

    profile     = forms.CharField(
        label = u"プロフィール",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 6,"cols":100, "maxlength":480})
    )
    email       = forms.EmailField(
        label = "メールアドレス(非公開、連絡用)",
        required = True
    )
    tw_name     = forms.CharField(
        label = "Twitter (@以降)",
        required = False
    )
    fb_addr     = forms.CharField(
        label = "Facebook (ID)",
        required = False,
        widget=forms.TextInput(attrs={'placeholder':u'http://facebook.com/以降のID'})
    )
    site_addr   = forms.URLField(
        label = "サイト、ブログURL",
        required = False,
    )

    def clean_user_alias(self):
        user_alias = self.cleaned_data['user_alias']
        if not re.match(ur"^[A-Za-z0-9_]+$", user_alias):
            raise forms.ValidationError(u'利用できるのは英数字とアンダーバーのみです。')
        pre_dev = Developer.getByAlias(user_alias)
        if pre_dev:
            raise forms.ValidationError(u"そのIDはすでに使われています")
        return user_alias

class RegistFormFirst(RegistForm):
    def __init__(self, *args, **kwargs):
        super(RegistFormFirst, self).__init__(*args, **kwargs)
        self.fields.pop('profile')
        self.fields.pop('tw_name')
        self.fields.pop('fb_addr')
        self.fields.pop('site_addr')



class RegistFormUpdate(RegistForm):
    def __init__(self, *args, **kwargs):
        super(RegistFormUpdate, self).__init__(*args, **kwargs)
        self.fields.pop('user_alias')
        
    def setParams(self, params):
        #return dir(params)
        for key in self.fields.keys():
          if hasattr(params, key):
            self.fields[key].initial = getattr(params, key)
        return self
    


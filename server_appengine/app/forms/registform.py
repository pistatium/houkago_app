#coding: utf-8

from django import forms
# -- Rules of validation -------------------------------
# ------------------------------------------------------

# regist用バリデーションルール
class RegistForm(forms.Form):
    uname       = forms.CharField(
        label = u"開発者名",
        max_length = 25,
        required = True,
        initial= None
    )

    profile     = forms.CharField(
        label = u"プロフィール",
        max_length = 2048, 
        required = False, 
        widget=forms.Textarea
    )
    email       = forms.EmailField(
        label = "メールアドレス(非公開)",
        required = True
    )
    tw_name     = forms.CharField(
        "Twitter (@以降)",
        required = False
    )
    fb_addr     = forms.CharField(
        "Facebook",
        required = False
    )
    site_addr   = forms.URLField(
        label = "サイト、ブログURL",
        required = False
    )
    

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
        
    def setParams(self, params):
        #return dir(params)
        for key in self.fields.keys():
          if hasattr(params, key):
            self.fields[key].initial = getattr(params, key)
        return self
    


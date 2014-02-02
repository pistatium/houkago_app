#coding: utf-8

from django import forms

# -- Rules of validation -------------------------------
# ------------------------------------------------------

from app.libs.arrays import platforms, show_status

# regist用バリデーションルール
class AppForm(forms.Form):

    platform = forms.ChoiceField(
        label   = u"プラットフォーム",
        choices = platforms, 
        required = True, 
    )
    app_name = forms.CharField(
        label = "アプリ名(必須)",
        max_length = 32, 
        required = True,
    )
    tagline = forms.CharField(
        label = "アプリのキャッチコピー（必須）",
        widget=forms.TextInput(attrs={'maxlength':'40'})
    )
    pr_summary = forms.CharField(
        label = u"アプリ概要(必須)",
        max_length = 480, 
        required = True, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480})
    )
    package_name = forms.CharField(
        label = "アプリパッケージ名(必須)",
        required = True,
    )
    dl_link = forms.URLField(
        label = "ダウンロード/サイト URL(必須)",
        required = True,
        verify_exists = True,
    )

    why_create = forms.CharField(
        label = u"アプリを作った理由",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480})
    )
    product_point = forms.CharField(
        label = u"開発に力を入れたポイント",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480})
    )
    status = forms.ChoiceField(
        label   = u"表示",
        choices = show_status, 
    )


class AppFormUpdate(AppForm):
    def __init__(self, *args, **kwargs):
        super(AppFormUpdate, self).__init__(*args, **kwargs)
        self.fields.pop('platform')

    def setParams(self, params):
        #return dir(params)
        for key in self.fields.keys():
          if hasattr(params, key):
            self.fields[key].initial = getattr(params, key)
        return self


"""
    developer_id  = ndb.IntegerProperty()
    app_name      = ndb.StringProperty()
    package_name  = ndb.StringProperty()
    platform      = ndb.IntegerProperty()
    pr_summary    = ndb.StringProperty() # アプリ概要 
    why_create    = ndb.StringProperty() # アプリを作った理由
    product_point = ndb.StringProperty() # 開発に力を入れたポイント
    status        = ndb.IntegerProperty(default = 1)
    created_at    = ndb.DateTimeProperty(auto_now_add = True)
    updated_at    = ndb.DateTimeProperty(auto_now = True)
    thumb_nail    = ndb.StringProperty()
    app_image     = ndb.StringProperty()
    category      = ndb.IntegerProperty()
    
"""
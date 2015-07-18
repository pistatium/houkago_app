#coding: utf-8

from django import forms

# -- Rules of validation -------------------------------
# ------------------------------------------------------

from app.libs.arrays import platforms, categories, show_status

# regist用バリデーションルール
class AppForm(forms.Form):

    platform = forms.ChoiceField(
        label   = u"プラットフォーム(変更不可)",
        choices = platforms, 
        required = True, 
    )
    app_name = forms.CharField(
        label = "アプリ名(必須)",
        max_length = 32, 
        required = True,
    )
    category = forms.ChoiceField(
        label   = u"カテゴリ",
        choices = categories, 
        required = False, 
    )
    tagline = forms.CharField(
        label = "アプリのキャッチコピー（必須）",
        widget=forms.TextInput(attrs={'maxlength':'40','placeholder':'アプリの魅力を端的に'})
    )
    pr_summary = forms.CharField(
        label = u"アプリ概要(必須)",
        max_length = 480, 
        required = True, 
        widget=forms.Textarea(attrs={"rows": 6,"cols":100, "maxlength":480})
    )
    package_name = forms.CharField(
        label = "アプリパッケージ名(必須)",
        required = True,
        widget=forms.TextInput(attrs={'placeholder':'Webアプリの場合はURL'})
    )
    dl_link = forms.URLField(
        label = "ダウンロード/サイト URL(必須)",
        required = True,
    )
    src_url = forms.URLField(
        label = "ソースを公開している場合(Gifhubなど)のURLを",
        required = False,
    )

    why_create = forms.CharField(
        label = u"このアプリを作った理由を教えて下さい！",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480,
            'placeholder':'開発のきっかけ、開発に対する想いなど'})
    )
    product_point = forms.CharField(
        label = u"このアプリを開発する上で力を入れたポイントは？",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480,
            'placeholder':'開発でこだわった点、上手く行かなくて苦労した点など'})
    )
    target_user = forms.CharField(
        label = u"どんなユーザーに使って欲しいですか？",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480,
            'placeholder':'ターゲットとしたユーザー、利用想定シーンなど具体的に'})
    )
    technology = forms.CharField(
        label = u"使用している言語、ライブラリなどは何ですか？",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480,
            'placeholder':'使ったライブラリなど。採用理由等もあれば'})
    )
    dev_scale = forms.CharField(
        label = u"アプリ開発の規模はどれくらいですか?",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480,
            'placeholder':'構想、開発にかかった期間など'})
    )
    future_vision = forms.CharField(
        label = u"今後のアップデートの展望を教えて下さい！",
        max_length = 480, 
        required = False, 
        widget=forms.Textarea(attrs={"rows": 4,"cols":100, "maxlength":480,
            'placeholder':'改修予定など'})
    )
    status = forms.ChoiceField(
        label   = u"表示",
        choices = show_status, 
    )
    def clean_category(self):
        category = self.cleaned_data['category']
        if category:
            return int(category)
        



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
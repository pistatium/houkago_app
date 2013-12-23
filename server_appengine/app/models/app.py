#coding: utf-8

from google.appengine.ext import ndb


class App(ndb.Model):
    developer_id  = ndb.IntegerProperty()
    app_name      = ndb.StringProperty()
    package_name  = ndb.StringProperty()
    platform      = ndb.IntegerProperty()
    pr_summar     = ndb.StringProperty() # アプリ概要 
    why_create    = ndb.StringProperty() # アプリを作った理由
    product_point = ndb.StringProperty() # 開発に力を入れたポイント
    status        = ndb.IntegerProperty(default = 1)
    created_at    = ndb.DateTimeProperty(auto_now_add = True)
    updated_at    = ndb.DateTimeProperty(auto_now = True)
    thumb_nail    = ndb.StringProperty()
    app_image     = ndb.StringProperty()
    category      = ndb.IntegerProperty()
#coding: utf-8

from google.appengine.ext import ndb


class App(ndb.Model):
    developer_id  = ndb.StringProperty()
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
    
    @classmethod
    def save(cls, params, instance = None):
        app = cls.create(params, instance)
        app.put()
        return app

    @classmethod
    def create(cls, params, instance = None):
        if not instance:
            instance = cls()
        params["platform"] = int(params["platform"])
        params["status"]   = int(params["status"])
        instance.populate(**params)
#        instance.populate(
#            developer_id = params["developer_id"],
#            app_name     = params["app_name"],
#            package_name = params["package_name"],
#            platform     = int(params["platform"]),
#            pr_summary   = params["pr_summary"],
#            why_create   = params["why_create"],
#            product_point= params["product_point"],
#            status       = int(params["status"]),
#        )
        return instance

    @classmethod
    def getById(cls, appid):
        return cls.get_by_id(appid)


    @classmethod
    def getQuery(cls):
        query = cls.query()
        return query


    @classmethod
    def getQueryByDeveloper(cls, developer_id, platform = None):
        query = cls.query(cls.developer_id == developer_id)
        if platform:
            query.query(cls.platform == platform)
        return query

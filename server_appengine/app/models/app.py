#coding: utf-8
from __future__ import absolute_import

from google.appengine.ext import ndb

from ..libs.utils import cache


class App(ndb.Model):
    developer_id  = ndb.IntegerProperty()
    app_name      = ndb.StringProperty()
    dl_link       = ndb.StringProperty()
    src_url       = ndb.StringProperty()
    package_name  = ndb.StringProperty()
    platform      = ndb.IntegerProperty()
    tagline       = ndb.StringProperty() # キャッチフレーズ
    pr_summary    = ndb.StringProperty() # アプリ概要 
    why_create    = ndb.StringProperty() # アプリを作った理由
    product_point = ndb.StringProperty() # 開発に力を入れたポイント
    target_user   = ndb.StringProperty() # どんなユーザーをターゲットにしているか
    technology    = ndb.StringProperty() # 使用技術、ライブラリ
    dev_scale     = ndb.StringProperty() # 開発規模
    future_vision = ndb.StringProperty() # 今後の展望
    affiriate_point = ndb.IntegerProperty(default=1) # アフィリエイトポイント
    affiriate_point_total = ndb.IntegerProperty(default=0) # アフィリエイトポイント 累計 初期値は0
    status        = ndb.IntegerProperty(default = 1)
    created_at    = ndb.DateTimeProperty(auto_now_add = True)
    updated_at    = ndb.DateTimeProperty(auto_now = True)
    thumbnail    = ndb.StringProperty()
    category      = ndb.IntegerProperty()
    # イチオシアプリを数値管理 1,2,3
    creator_push  = ndb.IntegerProperty()
    
    @classmethod
    def save(cls, params, instance = None):
        app = cls.create(params, instance)
        app.put()
        return app

    @classmethod
    def create(cls, params, instance = None):
        if not instance:
            instance = cls()
        if "platform" in params:
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
        if appid:
            return cls.get_by_id(appid)

    @classmethod
    def update_push(cls, developer_id, params):
        """ 押しアプリ更新"""
        cls.clear_push(developer_id, params["platform"])
        best_apps = []
        best_app_key = set([])
        for i in range(1, 4):
            key = "best_" + str(i) + "_app"
            if params[key] in best_app_key: 
                continue
            app = App.getById(params[key])
            if not app: continue
            if not app.developer_id == developer_id: continue
            if not app.platform  == int(params["platform"]): continue

            setattr(app, "creator_push", len(best_apps) + 1)
            best_apps.append(app)
            best_app_key.add(params[key])
        ndb.put_multi(best_apps)

    @classmethod
    def clear_push(cls, developer_id, platform):
        """押しアプリリセット"""
        apps = cls.query(
            cls.developer_id == developer_id,
            cls.platform     == int(platform),
            cls.creator_push > 0
        ).fetch()

        for app in apps:
            app.creator_push = None
        ndb.put_multi(apps)

    @classmethod
    def getQuery(cls):
        query = cls.query()
        return query


    @classmethod
    def getQueryByDeveloper(cls, developer_id, platform = None):
        query = cls.query(cls.developer_id == developer_id)
        if platform:
            query = query.filter(cls.platform == platform)
        return query
    
    @classmethod
    def getRecentQuery(cls, platform = None, cat_id = None):
        query = cls.query()
        query = query.filter(cls.status == 1)
        if platform is not None:
            query = query.filter(cls.platform == platform)
        if cat_id is not None:
            query = query.filter(cls.category == cat_id)
        return query.order(-cls.created_at)
    
    @classmethod
    def getPush(cls, developer_id, platform):
        query = cls.query(cls.developer_id == developer_id)
        query = query.filter(cls.platform == platform)
        return query.order(-cls.creator_push).fetch(3)


    @classmethod
    @cache(3600)
    def getPickup(cls, count=4):
        query = cls.query(cls.status == 1)
        apps = query.order(-cls.affiriate_point).order(-cls.affiriate_point_total).fetch(count)
        if not apps:
            return []
        # 一番先頭に来たアプリはポイントを減らす
        first_app = apps[0]
        if first_app.affiriate_point > 1:
            first_app.affiriate_point -= 1
            first_app.put()
        return apps

# coding: utf-8

from google.appengine.ext import ndb


class User(ndb.Model):    
    """ 一般ユーザー"""
       
    user_id      = ndb.StringProperty()
    user_alias   = ndb.StringProperty()
    uname        = ndb.StringProperty()
    status       = ndb.IntegerProperty(default = 0)
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    updated_at   = ndb.DateTimeProperty(auto_now = True)
    profile      = ndb.TextProperty()
    email        = ndb.StringProperty()
    site_addr    = ndb.StringProperty()
    billing      = ndb.IntegerProperty(default = 0) # 0 未課金

    @classmethod
    def save(cls, params, instance=None):
        developer = cls.create(params, instance)
        developer.put()
        return developer

    @classmethod
    def create(cls, params, instance=None):
        if not instance:
            instance = cls()
        instance.populate(**params)
        return instance

    @classmethod
    def getByUserId(cls, user_id):
        query = cls.query(cls.user_id == user_id)
        data = query.get()
        if data:
            return data
        return False

    @classmethod
    def getByAlias(cls, user_alias):
        query = cls.query(cls.user_alias == user_alias)
        data = query.get()
        if data:
            return data
        return False

    @classmethod
    def getQuery(cls):
        query = cls.query().order(-cls.created_at)
        return query

#coding: utf-8
from google.appengine.ext import ndb

class UseApi(ndb.Model):
    developer_id = ndb.IntegerProperty()
    client_name  = ndb.StringProperty()
    # 利用詳細
    description  = ndb.StringProperty()
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    status       = ndb.IntegerProperty(default = 1)

    @classmethod
    def getQuery(cls, developer_id):
    	return cls().query(cls.developer_id == developer_id)

    @classmethod
    def save(cls, params, instance = None):
        useapi = cls.create(params, instance)
        useapi.put()
        return useapi

    @classmethod
    def create(cls, params, instance=None):
        if not instance:
            instance = cls()
        instance.populate(**params)
        return instance
#coding: utf-8
#from django import forms
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
#from app.libs.utils import cache


class Developer(ndb.Model):
    # user id given by google
    user_id      = ndb.StringProperty()
    user_alias   = ndb.StringProperty()

    uname        = ndb.StringProperty()
    #いいねしたユーザー
    plused_user  = ndb.IntegerProperty(repeated=True)
    # レス数
    status       = ndb.IntegerProperty(default = 0)
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    updated_at   = ndb.DateTimeProperty(auto_now = True)
    profile      = ndb.TextProperty()
    email        = ndb.StringProperty()
    tw_name      = ndb.StringProperty()
    fb_addr      = ndb.StringProperty()
    site_addr    = ndb.StringProperty()
    best_apps_id = ndb.IntegerProperty(repeated=True)
    billing      = ndb.IntegerProperty(default = 0) # 0 未課金

    @classmethod
    def save(cls, params, instance = None):
        developer = cls.create(params, instance)
        developer.put()
        return developer

    @classmethod
    def create(cls, params, instance=None):
        if not instance:
            instance = cls()
        instance.populate(**params)
#        instance.populate(
#            user_id    = params['user_id'],
#            uname      = params['uname'],
#            profile    = params['profile'],
#            email      = params['email'],
#            tw_name    = params['tw_name'],
#            fb_addr    = params['fb_addr'],
#            site_addr  = params['site_addr'],
#            status     = params['status'],
#        )
        return instance
    
    @classmethod
    def getByUserId(cls, user_id):
        query = cls.query(cls.user_id == user_id)
        data = query.get()
        if data:
          return data
        return False

    #@cache
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

    '''    
    @classmethod
    def addRes(cls, thread_id):
        thread = ThreadModel.get_by_id(thread_id)
        thread.res_count += 1
        thread.put()
        return thread

    @classmethod
    def get(cls, params):
        if params["status"] == 2:
          q = cls.query()
        else:
          q = cls.query(cls.status == params["status"])
                  
        page_count = params['count']
        page_num = params['page']
        sortby = params['sortby']
        reverse = False
        if params['reverse']== 1:
            reverse = True
        q = _sortQuery(cls, q, sortby, reverse)

        p = GAEPaginator(q, page_count)
        return p.page(page_num)
    '''

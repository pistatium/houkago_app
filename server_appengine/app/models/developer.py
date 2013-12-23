#coding: utf-8
#from django import forms
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError



class Developer(ndb.Model):
    user_id     = ndb.StringProperty()
    uname        = ndb.StringProperty()
    #いいねしたユーザー
    plused_user  = ndb.IntegerProperty(repeated=True)
    # レス数
    status       = ndb.IntegerProperty(default = 1)
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    updated_at   = ndb.DateTimeProperty(auto_now = True)
    profile      = ndb.TextProperty()
    email        = ndb.StringProperty()
    tw_name      = ndb.StringProperty()
    fb_addr      = ndb.StringProperty()
    site_addr    = ndb.StringProperty()
    best_apps_id = ndb.IntegerProperty(repeated=True)
    thumb_nail   = ndb.StringProperty()
    billing      = ndb.IntegerProperty(default = 0) # 0 未課金

    @classmethod
    def create(cls, params, is_commit = True):

        developer = DeveloperModel(
            user_id    = params['user_id'],
            uname      = params['uname'],
            profile    = params['profile'],
            email      = params['email'],
            tw_name    = params['tw_name'],
            #fb_addr    = params['fb_addr'],
            site_addr  = params['site_addr'],
            status     = params['status'],
        )
        if is_commit:
            developer.put()
        return developer
    
    @classmethod
    def getById(cls, developer_id):
        query = cls.query(cls.user_id == developer_id)
        data = query.get()
        if data:
          return data
        return False
    
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

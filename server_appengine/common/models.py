#coding: utf-8
#from django import forms
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from datetime import datetime
from google.appengine.datastore.datastore_query import Cursor
from libs.gae_paginator import GAEPaginator

from django.db import models


class DeveloperModel(ndb.Model):
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


class AppModel(ndb.Model):
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

class ThumbnailModel(ndb.Model):
    image         = ndb.BlobProperty()
    mimetype      = ndb.StringProperty()
    developer_id  = ndb.IntegerProperty()
    thumb_type    = ndb.IntegerProperty()
    created_at    = ndb.DateTimeProperty(auto_now_add = True)
    updated_at    = ndb.DateTimeProperty(auto_now = True)


class PreUser(ndb.Model):
    user_mail     = ndb.StringProperty()
    send_status   = ndb.IntegerProperty(default = 0) 
    created_at    = ndb.DateTimeProperty(auto_now_add = True)
    updated_at    = ndb.DateTimeProperty(auto_now = True)

    @classmethod
    def getByMail(cls, email):
        query = cls.query(cls.user_mail == email)
        user = query.get()
        if not user:
          user = PreUser(user_mail = email)
        return user
        

###########################################################################
###########################################################################

def _sortQuery(cls, query, sortby, reverse = False):
    # created|updated|count|evaluated    
    if sortby == 'created':
        if reverse:
            q = query.order(cls.created_at)
        else:
            q = query.order(-cls.created_at)

    elif sortby == 'updated':
        if reverse:
            q = query.order(cls.updated_at)
        else :
            q = query.order(-cls.updated_at)
            
    elif sortby == 'evaluated':
        if reverse:
            q = query.order(-cls.total_count)
        else :
            q = query.order(cls.total_count)
    return q

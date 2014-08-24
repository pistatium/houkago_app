#coding: utf-8
#from django import forms
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from datetime import datetime, timedelta


THREAD_MAX = 500

class IdeaThread(ndb.Model):
    user_id     = ndb.IntegerProperty()
    # スレタイ
    title        = ndb.StringProperty()
    # いいねしたユーザー
    plused_user  = ndb.IntegerProperty(repeated=True)
    minused_user  = ndb.IntegerProperty(repeated=True)
    total_count = ndb.IntegerProperty(default = 0)
    # レス数
    res_count    = ndb.IntegerProperty(default = 1)
    status       = ndb.IntegerProperty(default = 0)  # 0 待ち　1　人気　-1 管理削除　-2　自然削除
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    updated_at   = ndb.DateTimeProperty(auto_now = True)
    category     = ndb.IntegerProperty(default = 0)
    res_one_id   = ndb.IntegerProperty()
    summary      = ndb.StringProperty(default = '')
    uname        = ndb.StringProperty(default = u'')
    
    @classmethod
    def create(cls, params):
        thread = IdeaThread(
            user_id   = params['user_id'],
            title     = params['title'],
            category  = int(params['category']),
            summary   = params['body'][:180] + u"\n……",
            uname     = params['uname']
        )
        thread.put()
        return thread
    
    def insertResOneId(self, res_one_id):
        self.res_one_id = int(res_one_id)
        self.put()
        
    @classmethod
    def addRes(cls, thread_id):
        thread = IdeaThread.get_by_id(thread_id)
        thread.res_count += 1
        thread.put()
        return thread

    @classmethod
    def getById(cls, thread_id):
        query = IdeaThread.query(IdeaThread.id == thread_id)
        data = query.get()
        if data:
          return data
        return False
    
    @classmethod
    def get(cls, params):
        if params["status"] == 2:
          q = cls.query()
        else:
          q = cls.query(cls.status == params["status"])
                  
        sortby = params['sortby']
        reverse = False
        if params['reverse']== 1:
            reverse = True
        q = _sortQuery(cls, q, sortby, reverse)

        return q

    @classmethod
    def evaluate(self, thread_id, user_id, is_plus):
        ''' いいね追加 '''
        thread = IdeaThread.get_by_id(thread_id)
        if user_id in thread.plused_user:
            return False
        if user_id in thread.minused_user:
            return False
        
        if is_plus:
            thread.plused_user.append(user_id)
            thread.total_count += 1
        else:
            thread.minused_user.append(user_id)
        if thread.status >= 0 and thread.total_count >= 4:
            thread.status = 1
            
        # not update timestamp
        #thread.__dict__["auto_now"] = False;

        thread.put()
        return thread

    @classmethod
    def getDeletable(cls):
        now_date = datetime.now()
        del_date = now_date - timedelta(days=90)
        threads = cls.query(cls.status == 0).filter(cls.updated_at < del_date).order(cls.updated_at).fetch(3)
        return threads


'''
    Resを管理するモデル
'''
class IdeaRes(ndb.Model):
    user_id     = ndb.StringProperty()
    number      = ndb.IntegerProperty(default = 1)
    body        = ndb.TextProperty()
    uname        = ndb.StringProperty(default = '匿名かまってちゃん')
    text_format = ndb.IntegerProperty(default = 0)
    plused_user = ndb.IntegerProperty(repeated=True)
    minused_user= ndb.IntegerProperty(repeated=True)
    total_count = ndb.IntegerProperty(default = 0)
    thread_id   = ndb.IntegerProperty(default = 0)
    created_at = ndb.DateTimeProperty(auto_now_add = True)
    updated_at  = ndb.DateTimeProperty(auto_now = True)

    def donadona(self):
        self.body  = "このレスは諸事情によりドナドナされました。"
        self.uname = "(Deleted)"
        self.total_count = -1000
        self.put()
        
    @classmethod
    def create(cls, params, res_count = None):
        thread_id = int(params['thread_id'])
        
        if res_count is None:
            thread = IdeaThread.get_by_id(thread_id)
            if thread:
                res_count = thread.res_count
                if res_count >= THREAD_MAX:
                    return None
            else:
                res_count = 0

        res = IdeaRes(
            user_id   = params['user_id'],
            body      = params['body'],
            uname     = params['uname'],
            thread_id = thread_id,
            number = res_count + 1
        )
        res.put()
        return res

    @classmethod
    def getByThreadId(cls, params):
        thread_id = int(params["thread_id"])
        q = cls.query(cls.thread_id == thread_id).order(cls.number)

        return q

        
    @classmethod
    def evaluate(self, g_res_id, user_id, is_plus):
        ''' いいね追加 '''
        res = IdeaRes.get_by_id(g_res_id)
        
        if user_id in res.plused_user:
            return False
        if user_id in res.minused_user:
            return False 
        
        if is_plus:
            res.plused_user.append(user_id)
            res.total_count += 1
        else:
            res.minused_user.append(user_id)
            
        res.put()
        return res

'''
    userを管理するモデル
'''
class UserModel(ndb.Model):
    # device id
    device       = ndb.StringProperty()
    # device key
    device_key          = ndb.StringProperty()
    # user evaluate
    plus_count   = ndb.IntegerProperty()
    minus_count  = ndb.IntegerProperty()
    # plus_count - minus_count
    rate         = ndb.IntegerProperty()
    # timestamp
    last_action  = ndb.DateTimeProperty()
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    updated_at   = ndb.DateTimeProperty(auto_now = True)
    # is user paid monthly
    is_paid      = ndb.IntegerProperty(default = 0)
    
    @classmethod
    def get(cls, user_id):
        query = UserModel.query(UserModel.device == user_id)
        data = query.get()
        if data:
          return data
        return False
    
    # last_actionを更新
    def doneAction(self):
        self.last_action = datetime.now()
        self.put()
        
    def registNewDevice(self, user_id, device_key):
        try:
          model = UserModel(
            device_key    = device_key,
            device = user_id,
            plus_count = 0,
            minus_count = 0,
            rate = 0,
            last_action = datetime.now(),
          )
          model.put()
        except BadValueError,e:
            return False
        return True    


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

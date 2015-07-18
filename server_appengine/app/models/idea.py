#coding: utf-8
#from django import forms
from google.appengine.ext import ndb
from datetime import datetime, timedelta


THREAD_MAX = 500

class IdeaThread(ndb.Model):
    user_id     = ndb.IntegerProperty()
    title        = ndb.StringProperty()
    # いいねしたユーザー
    plused_user  = ndb.IntegerProperty(repeated=True)
    # 評価数
    total_count = ndb.IntegerProperty(default = 0)
    # レス数
    comment_count    = ndb.IntegerProperty(default = 1)
    status       = ndb.IntegerProperty(default = 1) 
    created_at   = ndb.DateTimeProperty(auto_now_add = True)
    updated_at   = ndb.DateTimeProperty(auto_now = True)
    category     = ndb.IntegerProperty(default = 0)
    comment_one_id   = ndb.IntegerProperty()
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
    
    def insertCommentOneId(self, comment_one_id):
        self.comment_one_id = int(comment_one_id)
        self.put()
        
    @classmethod
    def addComment(cls, thread_id):
        thread = IdeaThread.get_by_id(thread_id)
        thread.comment_count += 1
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
    def getQuery(cls, sortby="updated", reverse=False):
        q = cls.query(cls.status == 1)
        q = _sortQuery(cls, q, sortby, reverse)
        return q

    @classmethod
    def evaluate(self, thread_id, user_id):
        ''' いいね追加 '''
        thread = IdeaThread.get_by_id(thread_id)
        if user_id in thread.plused_user:
            return False
        if user_id in thread.minused_user:
            return False
        
        thread.plused_user.append(user_id)
        thread.total_count += 1
        if thread.status >= 0 and thread.total_count >= 4:
            thread.status = 1

        thread.put()
        return thread



'''
    Commentを管理するモデル
'''
class IdeaComment(ndb.Model):
    user_id     = ndb.StringProperty()
    number      = ndb.IntegerProperty(default = 1)
    body        = ndb.TextProperty()
    uname        = ndb.StringProperty(default = '')
    text_format = ndb.IntegerProperty(default = 0)
    plused_user = ndb.IntegerProperty(repeated=True)
    minused_user= ndb.IntegerProperty(repeated=True)
    total_count = ndb.IntegerProperty(default = 0)
    thread_id   = ndb.IntegerProperty(default = 0)
    created_at = ndb.DateTimeProperty(auto_now_add = True)
    updated_at  = ndb.DateTimeProperty(auto_now = True)

        
    @classmethod
    def create(cls, params, comment_count = None):
        thread_id = int(params['thread_id'])
        
        if comment_count is None:
            thread = IdeaThread.get_by_id(thread_id)
            if thread:
                comment_count = thread.comment_count
                if comment_count >= THREAD_MAX:
                    return None
            else:
                comment_count = 0

        comment = IdeaComment(
            user_id   = params['user_id'],
            body      = params['body'],
            uname     = params['uname'],
            thread_id = thread_id,
            number = comment_count + 1
        )
        comment.put()
        return comment

    @classmethod
    def getByThreadId(cls, params):
        thread_id = int(params["thread_id"])
        q = cls.query(cls.thread_id == thread_id).order(cls.number)

        return q

        
    @classmethod
    def evaluate(self, g_comment_id, user_id, is_plus):
        ''' いいね追加 '''
        comment = IdeaComment.get_by_id(g_comment_id)
        
        if user_id in comment.plused_user:
            return False
        if user_id in comment.minused_user:
            return False 
        
        if is_plus:
            comment.plused_user.append(user_id)
            comment.total_count += 1
        else:
            comment.minused_user.append(user_id)
            
        comment.put()
        return comment


def _sortQuery(cls, query, sortby, reverse = False):
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

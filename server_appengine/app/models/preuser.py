#coding: utf-8
from google.appengine.ext import ndb

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
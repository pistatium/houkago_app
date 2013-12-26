#coding: utf-8
from google.appengine.ext import ndb

class ThumbnailModel(ndb.Model):
    image         = ndb.BlobProperty()
    mimetype      = ndb.StringProperty()
    developer_id  = ndb.IntegerProperty()
    thumb_type    = ndb.IntegerProperty()
    created_at    = ndb.DateTimeProperty(auto_now_add = True)
    updated_at    = ndb.DateTimeProperty(auto_now = True)
    
    
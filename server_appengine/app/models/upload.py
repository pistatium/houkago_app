#coding: utf-8
from django.db import models
from google.appengine.ext import ndb

class UploadModel(models.Model):
    file = models.ImageField(
    	upload_to=None,
    	height_field = 512,
    	

    	)

class ProfImage(ndb.Model):
	image         = ndb.BlobProperty()
	developer_id  = ndb.StringProperty()
	created_at    = ndb.DateTimeProperty(auto_now_add = True)
	updated_at    = ndb.DateTimeProperty(auto_now = True)
	content_type  = ndb.StringProperty()

    






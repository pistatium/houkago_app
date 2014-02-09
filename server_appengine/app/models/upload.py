#coding: utf-8
from django.db import models
from google.appengine.ext import ndb

class UploadModel(models.Model):
    file = models.ImageField(
    	upload_to=None,
    	

    )


class ProfImage(ndb.Model):
	image         = ndb.BlobProperty()
	developer_id  = ndb.IntegerProperty()
	created_at    = ndb.DateTimeProperty(auto_now_add = True)
	updated_at    = ndb.DateTimeProperty(auto_now = True)
	content_type  = ndb.StringProperty()

	@classmethod
	def getByDeveloper(cls, developer_id):
		query = cls.query(cls.developer_id == developer_id)
		img = query.get()
		if img:
			return img
		return None

	@classmethod
	def getEntity(cls, developer_id):
		img = cls.getByDeveloper(developer_id)
		if img:
			return img
		return cls(
                developer_id = developer_id
		)


class AppImage(ndb.Model):
	image         = ndb.BlobProperty()
	app_id        = ndb.IntegerProperty()
	created_at    = ndb.DateTimeProperty(auto_now_add = True)
	updated_at    = ndb.DateTimeProperty(auto_now = True)
	content_type  = ndb.StringProperty()

	@classmethod
	def getByAppId(cls, app_id):
		query = cls.query(cls.app_id == app_id)
		img = query.get()
		if img:
			return img
		return None

	@classmethod
	def getEntity(cls, app_id):
		img = cls.getByAppId(app_id)
		if img:
			return img
		return cls(
                app_id = app_id,
		)
    






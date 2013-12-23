from django.conf.urls.defaults import *

urlpatterns = patterns('webfront.views_home',
	(r'^demo', 'demo'),
	(r'^pre_complete', 'pre_complete'),
	(r'^pre', 'pre'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

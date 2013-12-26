from django.conf.urls.defaults import *

urlpatterns = patterns('app.views.home.views',
	(r'^demo', 'demo'),
	(r'^pre_complete', 'pre_complete'),
	(r'^pre', 'pre'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

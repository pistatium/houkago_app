from django.conf.urls.defaults import *

urlpatterns = patterns('webfront.views_home',
	(r'^demo', 'demo'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

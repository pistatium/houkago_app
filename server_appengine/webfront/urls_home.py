from django.conf.urls.defaults import *

urlpatterns = patterns('webfront.views_home',
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

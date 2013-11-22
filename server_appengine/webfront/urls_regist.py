from django.conf.urls.defaults import *

urlpatterns = patterns('webfront.views_regist',
    (r'^/form', 'form'),
    (r'^/complete', 'complete'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

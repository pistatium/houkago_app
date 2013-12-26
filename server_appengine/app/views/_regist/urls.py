from django.conf.urls.defaults import *

urlpatterns = patterns('app.views.regist.views',
    (r'^/form', 'form'),
    (r'^/complete', 'complete'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

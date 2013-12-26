from django.conf.urls.defaults import *

urlpatterns = patterns('app.views.dev.views',
    (r'^/app_regist', 'app_regist'),
    (r'^/app_regist', 'app_edit'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

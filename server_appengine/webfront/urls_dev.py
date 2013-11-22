from django.conf.urls.defaults import *

urlpatterns = patterns('webfront.views_dev',
    (r'^/app_regist', 'app_regist'),
    (r'^/app_regist', 'app_edit'),
    (r'^/?$', 'index'),
    (r'^.*', 'notfound'),
)

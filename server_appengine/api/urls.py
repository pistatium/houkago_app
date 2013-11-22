from django.conf.urls.defaults import *

urlpatterns = patterns('api.views',
    (r'^regist$', 'regist'),
    (r'^make_thread$', 'makeThread'),
    (r'^get_thread$', 'getThread'),
    (r'^evaluate_thread$', 'evaluateThread'),
    (r'^make_res$', 'makeRes'),
    (r'^get_res$', 'getRes'),
    (r'^evaluate_res$', 'evaluateRes'),
    (r'^delete_thread$', 'deleteThread'),
    (r'^delete_res$', 'deleteRes'),
    (r'^.*', 'notfound'),
)

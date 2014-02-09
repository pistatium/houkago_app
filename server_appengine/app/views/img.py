#coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse 
from django.conf.urls.defaults import *
from django.template import RequestContext


from app.models.developer import Developer
from app.models.upload import ProfImage, AppImage
"""
Viewの共通前処理をするデコレータ
viewの引数にcontextが増えることに注意
"""
def custom_view(view):
    import functools
    @functools.wraps(view)
    def override_view(*args, **kwargs):
        request = args[0]        
        #user = users.get_current_user()
        #developer = None
        #if user:
        #    developer = Developer.getById(user.user_id())
        context = RequestContext(request,{
        #    "is_login": bool(user),
        #    "logout_page": reverse(views.regist.index),
        #    "developer" : developer,
        })
        kwargs["context"] = context
        return view(*args, **kwargs)
    return override_view

@custom_view
def user_icon(request, user_id, context):
    image = ProfImage.getByDeveloper(long(user_id))
    if not image:
        return HttpResponseRedirect("/img/material/user.png")
    return HttpResponse(image.image, image.content_type)


@custom_view
def app_icon(request, app_id, context):
    image = AppImage.getByAppId(long(app_id))
    if not image:
        return HttpResponseRedirect("/img/material/app.png")
    return HttpResponse(image.image, image.content_type)





#======================================================================================
''' 
 URL パターン
'''
urlpatterns = patterns(None,
    (r'user/icon/(\d+)/?$', user_icon),
    (r'app/icon/(\d+)?$', app_icon),
)
#coding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse 
from django.conf.urls.defaults import *
from django.template import RequestContext


from app.models.developer import Developer
from app.models.upload import ProfImage
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
    developer = Developer.getById(user_id)
    if not developer:
        return HttpResponseRedirect("/img/material/user.png")
    if not developer.thumbnail:
        return HttpResponseRedirect("/img/material/user.png")
    image = ProfImage.get_by_id(developer.thumbnail)
    if not image:
        return HttpResponseRedirect("/img/material/user.png")
    return HttpResponse(image.image, image.content_type)


@custom_view
def app_icon(request, app_id, context):
    return HttpResponseRedirect("/img/material/app.png")





#======================================================================================
''' 
 URL パターン
'''
urlpatterns = patterns(None,
    (r'user/icon/(\d+)/?$', user_icon),
    (r'app/icon/(\d+)?$', app_icon),
)
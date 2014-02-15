#coding: utf-8

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import *


from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.api import mail
from django.core.urlresolvers import reverse 

from hashlib import sha1, md5
from random import randint
from datetime import datetime, timedelta
from logging import debug

# import from project
from app.models.preuser import PreUser
from app.forms.preform import PreForm
from app.libs import utils
from app.libs.gae_paginator import GAEPaginator
from app.models.developer import Developer
from app.models.app import App
from app import views
from app.libs.arrays import platforms, get_platform_id
#from app.forms import registform
import syskey
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect


# -- Views  --------------------------------------------
# ------------------------------------------------------


"""
Viewの共通前処理をするデコレータ
viewの引数にcontextが増えることに注意
"""
def custom_view(view):
    import functools
    @functools.wraps(view)
    def override_view(*args, **kwargs):
        request = args[0]        
        user = users.get_current_user()
        developer = None
        if user:
            developer = Developer.getByUserId(user.user_id())
        context = RequestContext(request,{
            "is_login": bool(user),
            "logout_page": reverse(views.regist.index),
            "developer" : developer,
            "platforms" : platforms,
        })
        kwargs["context"] = context
        return view(*args, **kwargs)
    return override_view

@cache_page(60 * 15)
@custom_view
def index(request, context):
    context["developers"] = Developer.getQuery().fetch(10)
    context["recent_apps"] = {}
    for platform in platforms:
        apps = App.getRecentQuery(platform[0]).fetch(8)
        if apps:
            context["recent_apps"][platform[1]] = apps
    return render_to_response('webfront/index.html', context)

@cache_page(60 * 15)
@custom_view
def about(request, context):
    context["current_tab"] = "about"
    return render_to_response('webfront/about.html',context)

@cache_page(60 * 60)
@custom_view
def user_id(request, user_id, context):
    developer = Developer.get_by_id(user_id)
    if not developer:
        raise Http404
    return HttpResponseRedirect(reverse(user, args=[developer.user_alias]))

@cache_page(60 * 15)
@custom_view
def user(request, user_alias, context):
    developer = Developer.getByAlias(user_alias)
    if not developer:
        raise Http404
    app = App.getQueryByDeveloper(developer.key.id())
    context["developer"] = developer
    context["apps"] = app
    context["platforms"] = platforms
    return render_to_response('webfront/developer_detail.html',context)

@cache_page(60 * 15)
@custom_view
def app_list(request, plat_str, page, context):
    COUNT = 12
    platform = get_platform_id(plat_str)
    query = App.getRecentQuery(platform)
    p = GAEPaginator(query, COUNT)
    context["plat_str"] = plat_str
    context["page"] = page
    context["apps"] = p.page(page)
    return render_to_response('webfront/app_list.html',context) 

@cache_page(60 * 15)
@custom_view
def app_detail(request, app_id, context):
    app = App.getById(int(app_id))
    if not app or app.status != 1:
        raise Http404
    context["app"] = app
    developer = Developer.get_by_id(app.developer_id)
    #if not developer.status != 1:
    #    raise Http404
    context["developer"] = developer
    context["push_app"] = App.getPush(app.developer_id, app.platform)
    return render_to_response('webfront/app_detail.html',context)   

@cache_page(60 * 15)
def app_rss(request, platform = None):
    context = RequestContext(request,{
            "platforms" : platforms,
    })
    context["apps"] = App.getRecentQuery(platform).fetch(10)
    return render_to_response('webfront/app_rss.xml',context, mimetype="application/xml")  


#======================================================================================
''' 
 URL パターン
'''
urlpatterns = patterns(None,
    (r'^about/?$', about),
    (r'^user_id/(\d+)/?$' , user_id),
    (ur'^user/(\w+)/?$' , user),
    (r'^app_list/(\w+)/(\d+)?$' , app_list),
    (r'^app_detail/(\d+)/?$' , app_detail),
    (r'^rss.xml$', app_rss),
    (r'^/?$', index),
)
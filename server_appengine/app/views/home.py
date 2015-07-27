#coding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from google.appengine.api import users
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.conf.urls import patterns

# import from project
from app.libs.gae_paginator import GAEPaginator
from app.models.developer import Developer
from app.models.app import App
from app import views
from app.libs.arrays import platforms, get_platform_id, categories
# from app.forms import registform

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
        context = RequestContext(request, {
            "is_login": bool(user),
            "logout_page": reverse(views.regist.index),
            "developer": developer,
            "platforms": platforms,
        })
        kwargs["context"] = context
        return view(*args, **kwargs)
    return override_view


@custom_view
def index(request, context):
    context["developers"] = Developer.getQuery().fetch(4)
    context["recent_apps"] = {}
    pickups = App.getPickup()
    context["pickup_apps"] = pickups[0:2]
    context["pickup_apps_after"] = pickups[2:]
    context["has_more"] = {}
    context["apps"] = App.getRecentQuery().fetch(18)
    return render_to_response('webfront/index.html', context)


@custom_view
def about(request, context):
    context["current_tab"] = "about"
    return render_to_response('webfront/about.html', context)


@custom_view
def about_api(request, context):
    context["current_tab"] = "about"
    return render_to_response('webfront/about_api.html', context)

@custom_view
def pr_link(request, context):
    context["current_tab"] = "about"
    return render_to_response('webfront/pr_link.html', context)

@custom_view
def user_id(request, user_id, context):
    developer = Developer.get_by_id(user_id)
    if not developer:
        raise Http404
    return HttpResponseRedirect(reverse(user, args=[developer.user_alias]))


@custom_view
def user(request, user_alias, context):
    developer = Developer.getByAlias(user_alias)
    if not developer:
        raise Http404
    app = App.getQueryByDeveloper(developer.key.id())
    context["developer"] = developer
    context["apps"] = app
    context["platforms"] = platforms
    return render_to_response('webfront/developer_detail.html', context)

@custom_view
def user_list(request, page, context):
    COUNT = 50
    query = Developer.getQuery()
    p = GAEPaginator(query, COUNT)
    context["page"] = page
    context["developers"] = p.page(page)
    return render_to_response('webfront/user_list.html', context)

@custom_view
def app_list(request, plat_str, page, context):
    COUNT = 24
    platform = get_platform_id(plat_str)
    query = App.getRecentQuery(platform)
    p = GAEPaginator(query, COUNT)
    context["plat_str"] = plat_str
    context["page"] = page
    context["categories"] = categories
    context["apps"] = p.page(page)
    return render_to_response('webfront/app_list.html', context) 


@custom_view
def app_cat(request, plat_str, cat_id, page, context):
    COUNT = 24
    platform = get_platform_id(plat_str)
    query = App.getRecentQuery(platform, int(cat_id))
    p = GAEPaginator(query, COUNT)
    context["plat_str"] = plat_str
    context["cat_id"] = int(cat_id)
    context["categories"] = categories
    context["page"] = page
    context["apps"] = p.page(page)
    return render_to_response('webfront/app_list.html', context) 


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
    # 自身が含まれている可能性があるので +1件
    context["related_app"] = App.getRecentQuery(app.platform, app.category).fetch(3 + 1)
    return render_to_response('webfront/app_detail.html',context)   


@cache_page(60 * 15)
def app_rss(request, platform = None):
    context = RequestContext(request,{
            "platforms" : platforms,
    })
    context["apps"] = App.getRecentQuery(platform).fetch(50)
    return render_to_response('webfront/app_rss.xml',context, mimetype="application/xml")  

@cache_page(60 * 15)
def sitemap(request):
    context = RequestContext(request,{
    })
    context["apps"] = App.getRecentQuery(None)
    context["developers"] = Developer.getQuery()
    return render_to_response('webfront/sitemap.xml',context, mimetype="application/xml")  

#======================================================================================
''' 
 URL パターン
'''
urlpatterns = patterns(None,
    (r'^about/?$', about),
    (r'^about_api/?$', about_api),
    (r'^pr_link/?$', pr_link),
    (r'^user_id/(\d+)/?$' , user_id),
    (ur'^user/(\w+)/?$' , user),
    (ur'^user_list/(\d+)/?$' , user_list),
    (r'^app_list/(\w+)/(\d+)?$' , app_list),
    (r'^app_cat/(\w+)/(\d+)/(\d+)?$' , app_cat),
    (r'^app_cat/(\w+)//(\d+)?$' , app_cat),
    (r'^app_detail/(\d+)/?$' , app_detail),
    (r'^rss.xml$', app_rss),
    (r'^sitemap.xml$', sitemap),
    (r'^/?$', index),
)

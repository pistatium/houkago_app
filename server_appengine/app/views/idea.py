# coding: utf-8

from __future__ import absolute_import, division, print_function

from hashlib import sha1, md5
from random import randint
from datetime import datetime, timedelta
from logging import debug

from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse 
from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import *
from django.template import RequestContext
from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.api import memcache
from google.appengine.api import users

import syskey
# import from project
from app.models.developer import Developer
from app.models.user import User
from app.models.idea import Idea
from app.models.useapi import UseApi
from app.models.upload import ProfImage, AppImage
from app.libs import utils
from app.forms.appform import AppForm, AppFormUpdate
from app.forms.pushform import PushForm
from app.forms.uploadform import UploadForm
from app.forms.useapiform import UseApiForm
from app import views
from app.libs.arrays import platforms, show_status
from app.libs.filetransfers.api import prepare_upload

"""
Viewの共通前処理をするデコレータ
viewの引数にcontextが増えることに注意
"""
def custom_view(view):
    import functools
    @functools.wraps(view)
    @utils.login_required
    def override_view(*args, **kwargs):
        request = args[0]
        user = users.get_current_user()
        idea_user = User.getByUserId(user.user_id())
        # developerを兼ねる場合も
        developer = Developer.getByUserId(user.user_id())
        if not idea_user:
            return HttpResponseRedirect(reverse(views.idea.form))
        context = RequestContext(request,{
            "is_login": True,
            "logout_page": reverse(views.regist.index),
            "developer" : developer,
            "idea_user" : idea_user,
            "current_tab": "dev",
            "platforms": platforms,
            "show_status": show_status
        })
        kwargs["context"] = context
        return view(*args, **kwargs)
    return override_view

@custom_view
def index(view, context):
    context["ideas"] = Idea.getQuery().fetch(10)
    return render_to_response('webfront/idea_index.html',context)

@custom_view
def idea_list(request, page, context):
    query = Idea.getQuery()
    p = GAEPaginator(query, COUNT)
    context["page"] = page
    context["ideas"] = p.page(page)
    return render_to_response('webfront/idea_list.html',context)

@custom_view
def api_regist(request, context):
    context["form"] = UseApiForm()
    developer_id = context["developer"].key.id()
    context["use_api"] = UseApi.getQuery(developer_id)
    if request.method == 'POST':
        form = UseApiForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params["developer_id"] = developer_id
            useapi = UseApi.create(params)
            useapi.put()
            return HttpResponseRedirect(reverse(api_regist))
        else:
            context["form"] = form


    #apps = App.getQueryByDeveloper(context["developer"].key.id())
    #context["apps"] = apps
    return render_to_response('webfront/api_regist.html',context)


@utils.login_required
def register_complete(request):
    return render_to_response('webfront/regist_complete.html',{})

#======================================================================================
''' 
 URL パターン
'''

urlpatterns = patterns(None,
    (r'^/register/complete$', user_regist_complete),
    (r'^/register/$', user_regist),
    (r'^/edit/$', idea_edit),
    (r'^/create/$', idea_create),
    (r'^/idea/(\d+)', idea_detail),
    (r'^/idea_list/(\d+)?$', idea_list),
    (r'^/?$', index),
)

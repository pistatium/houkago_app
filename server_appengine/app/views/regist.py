#coding: utf-8
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse 
from django.views.decorators.cache import cache_page
from django.template import RequestContext

from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.api import memcache
from google.appengine.api import users

from hashlib import sha1, md5
from random import randint
from datetime import datetime, timedelta
from logging import debug

import syskey
# import from project
from app.models.developer import Developer
from app.libs import utils
from app.forms.registform import RegistFormFirst, RegistFormUpdate

from app import views
from pprint import pprint


"""
Viewの共通前処理をするデコレータ
viewの引数にcontextが増えることに注意
"""
def custom_view(view):
    import functools
    @functools.wraps(view)
    def override_view(request):        
        user = users.get_current_user()
        developer = None
        if user:
            developer = Developer.getByUserId(user.user_id())
        context = RequestContext(request,{
            "is_login": bool(user),
            "logout_page": reverse(views.regist.index),
            "developer" : developer,
            "current_tab": "dev",
        })
        return view(request, context)
    return override_view

# -- Views  --------------------------------------------
# ------------------------------------------------------
@custom_view
def index(request, context):
    user = users.get_current_user()
    if not user:
        context["login_url"] = users.create_login_url(reverse(form))
    else:
        context["user_id"] = user.user_id()
        context["logout_url"] = users.create_logout_url(reverse(index))
    return render_to_response('webfront/regist.html',context)

@utils.login_required
def form(request):
    context = RequestContext(request, {
        "form": "",
        "title": u"部員登録"
    })
    user = users.get_current_user()
    # 登録済みならリダイレクト
    if Developer.getByUserId(user.user_id()):
        return HttpResponseRedirect(reverse(views.dev.index))
    # POST
    if request.method == 'POST':
        #developer = models.DeveloperModel()
        form = RegistFormFirst(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params["user_id"] = user.user_id()
            params["status"]  = 1

            developer = Developer.save(params)
            return HttpResponseRedirect(reverse(complete))
        else:
            context["form"] = form
            return render_to_response('webfront/regist_form.html', context)
    # GET
    else:
        form = RegistFormFirst(initial={
            'uname': user.nickname(),
            'email': user.email()
        })
        context["form"] = form
        return render_to_response('webfront/regist_form.html', context)

@custom_view
def user_update(request, context={}):

    developer = context["developer"]

     # POST
    if request.method == 'POST':
        #developer = models.DeveloperModel()
        form = RegistFormUpdate(request.POST)

        if form.is_valid():
            params = form.cleaned_data
            params["user_id"] = developer.user_id
            params["status"]  = 1
            Developer.save(params, developer)
            return HttpResponseRedirect(reverse(views.dev.index))
        else:
            context["form"] = form
            return render_to_response('webfront/regist_form.html', context)

    # GET
    else:
        form = RegistFormUpdate()
        form.setParams(developer)

        context["form"] = form
        return render_to_response('webfront/regist_form.html', context)


@utils.login_required
def uploadProf(request):
    pass


@utils.login_required
def complete(request):
    return render_to_response('webfront/regist_complete.html',{})


def notfound(request):
    raise Http404

#======================================================================================
''' 
 URL パターン
'''
urlpatterns = patterns(None,
    (r'^/form/?$', form),
    (r'^/user_update/?$', user_update),
    (r'^/complete/?$', complete),
    (r'^/?$', index),
)

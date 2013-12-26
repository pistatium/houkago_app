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
from app.forms.registform import RegistForm

from app.views import dev

# -- Views  --------------------------------------------
# ------------------------------------------------------

def index(request):
    data = {
        "user_id"    : None,
        "login_url"  : "",
        "logout_url" : "",
    }
    user = users.get_current_user()
    if not user:
        data["login_url"] = users.create_login_url(reverse(form))
    else:
        data["user_id"] = user.user_id()
        data["logout_url"] = users.create_logout_url(reverse(index))

    return render_to_response('webfront/regist.html',data)

@utils.login_required
def form(request):
    context = RequestContext(request, {
        "form": "",
    })
    user = users.get_current_user()
    # 登録済みならリダイレクト
    if Developer.getById(user.user_id()):
        return HttpResponseRedirect(reverse(dev.index))
    # POST
    if request.method == 'POST':
        #developer = models.DeveloperModel()
        form = RegistForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params["user_id"] = user.user_id()
            params["status"]  = 1
            developer = Developer.create(params)
            developer.put()
            return HttpResponseRedirect(reverse(complete))
        else:
            context["form"] = form
            return render_to_response('webfront/regist_form.html', context)

    # GET
    else:
        form = RegistForm(initial={
            'uname': user.nickname(),
            'email': user.email()
        })
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
    (r'^/complete/?$', complete),
    (r'^/?$', index),
)

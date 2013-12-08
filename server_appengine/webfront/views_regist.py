#coding: utf-8

from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse 
from django.views.decorators.cache import cache_page

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
from common import models
from common import utils
from webfront import forms, views_dev


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
    data = {
        "form": "",
    }
    user = users.get_current_user()
    # 登録済みならリダイレクト
    if models.DeveloperModel.getById(user.user_id()):
        return HttpResponseRedirect(reverse(views_dev.index))
    # POST
    if request.method == 'POST':
        #developer = models.DeveloperModel()
        form = forms.RegistForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params["user_id"] = user.user_id()
            params["status"]  = 1
            developer = models.DeveloperModel.create(params)
            developer.put()
            return HttpResponseRedirect(reverse(complete))
        else:
            data["form"] = form.as_p()
            return render_to_response('webfront/regist_form.html', data)

    # GET
    else:
        form = forms.RegistForm(initial={
            'uname': user.nickname(),
            'email': user.email()
        })
        data["form"] = form.as_p()
        return render_to_response('webfront/regist_form.html', data)

@utils.login_required
def uploadProf(request):
    pass


@utils.login_required
def complete(request):
    return render_to_response('webfront/regist_complete.html',{})


def notfound(request):
    raise Http404

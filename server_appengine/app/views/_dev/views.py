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
from app import models
from app.libs import utils
from app import forms


# -- Views  --------------------------------------------
# ------------------------------------------------------

@utils.login_required
def index(request):
    return render_to_response('webfront/dev_index.html',{})

@utils.login_required
def app_regist(request):
    data = {
        "form": "",
    }
    user = users.get_current_user()
    if models.DeveloperModel.getById(user.user_id()):
        return HttpResponseRedirect("webfront/dev/home")
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
            return HttpResponseRedirect("webfront/regist_complete")
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
def app_edit(request):
    pass

@utils.login_required
def regist_complete(request):
    return render_to_response('webfront/regist_complete.html',{})

@utils.login_required
def notfound(request):
    raise Http404
           
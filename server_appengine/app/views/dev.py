#coding: utf-8

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


from hashlib import sha1, md5
from random import randint
from datetime import datetime, timedelta
from logging import debug

import syskey
# import from project
from app.models.developer import Developer
from app.models.app import App
from app.models.upload import ProfImage

from app.libs import utils
from app.forms.appform import AppForm, AppFormUpdate
from app.forms.pushform import PushForm
from app.forms.uploadform import UploadForm

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
        developer = Developer.getById(user.user_id())
        if not developer:
            return HttpResponseRedirect(reverse(views.regist.form))
        context = RequestContext(request,{
            "is_login": True,
            "logout_page": reverse(views.regist.index),
            "developer" : developer,
            "current_tab": "dev",
            "platforms": platforms,
            "show_status": show_status
        })
        kwargs["context"] = context
        return view(*args, **kwargs)
    return override_view

# -- Views  --------------------------------------------
# ------------------------------------------------------


@custom_view
def index(request, context):
    apps = App.getQueryByDeveloper(context["developer"].user_id)
    context["apps"] = apps
    return render_to_response('webfront/dev_index.html',context)

@custom_view
def app_detail(request, app_id, context={}):
    app = App.getById(int(app_id))
    if app is None:
        return HttpResponseRedirect(reverse(app_regist))
    context["app"] = app
    return render_to_response('webfront/app_detail.html',context)        

@custom_view
def app_regist(request, context):
     # POST
    if request.method == 'POST':
        #developer = models.DeveloperModel()
        form = AppForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params["developer_id"] = (context["developer"]).user_id
            app = App.create(params)
            app.put()
            return HttpResponseRedirect(reverse(app_detail, args=[app.key.id()]))
        else:
            context["form"] = form
            return render_to_response('webfront/regist_form.html', context)
    # GET
    else:
        form = AppForm(initial={
        })
        context["form"] = form
        return render_to_response('webfront/regist_form.html', context)

@custom_view
def app_update(request, app_id, context={}):
    app = App.getById(int(app_id))
    if app is None:
        return HttpResponseRedirect(reverse(app_regist))

     # POST
    if request.method == 'POST':
        #developer = models.DeveloperModel()
        form = AppFormUpdate(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            params["developer_id"] = (context["developer"]).user_id
            app = App.save(params, instance=app)
            app.put()
            return HttpResponseRedirect(reverse(index))
        else:
            context["form"] = form
            return render_to_response('webfront/regist_form.html', context)
    # GET
    else:
        form = AppFormUpdate()
        form.setParams(app)

        context["form"] = form
        return render_to_response('webfront/regist_form.html', context)

@custom_view
def update_push(request, context):
    if request.method == 'POST':
        
        form = PushForm(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            context["debug"] = params 
            developer_id = (context["developer"]).user_id
            App.update_push(developer_id, params)
    return HttpResponseRedirect(reverse(index))

@custom_view
def upload_img(request, context):
    view_url = reverse(upload_img)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            params = form.cleaned_data
            image = ProfImage(
                image = params["file"].read(),
                developer_id = (context["developer"]).user_id,
                content_type = params["file"].content_type
            )
            image.put()
            context["debug"] = image
            return render_to_response('webfront/index.html', context)
            #form.save()
            return HttpResponseRedirect(view_url)

    upload_url, upload_data = prepare_upload(request, view_url)
    form = UploadForm()
    context["form"] = form
    context["upload_url"] = upload_url
    context["upload_data"] = upload_data
    return render_to_response('webfront/upload_form.html', context)

@utils.login_required
def regist_complete(request):
    return render_to_response('webfront/regist_complete.html',{})

#======================================================================================
''' 
 URL パターン
'''

urlpatterns = patterns(None,
    (r'^/app_regist/?$', app_regist),
    (r'^/app_detail/(\d+)?$', app_detail),
    (r'^/app_update/(\d+)?$', app_update),
    (r'^/update_push/?$', update_push),
    (r'^/upload_img/?$', upload_img),
    (r'^/?$', index),
)

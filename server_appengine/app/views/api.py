#coding: utf-8

from json import dumps as jsonDump

from django.contrib.sites.models import Site

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse 
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from google.appengine.ext import ndb

from app.forms import apiform
from app.models.app import App
from app.libs import utils, arrays
from app.views.img import app_icon
from app.views.home import app_detail


def index(request):
    pass

@csrf_exempt
def recent_app(request, plat_str):
    return _makeJson(request, _recent_app, {"plat_str": plat_str,})

@csrf_exempt
def detail_app(request, app_id):
    return _makeJson(request, _detail_app, {"app_id": app_id,})

@csrf_exempt
def recent_developer(request):
    return _makeJson(request, _recent_developer)

##--------------------------------------------------------------

def _recent_app(request, option = {}):
    platform = arrays.get_platform_id(option["plat_str"])
    params = request.GET.copy()
    params["platform"] = platform
    form = apiform.RecentAppForm(params)
    if not form.is_valid():
        return {"status": -1, "thread_id":'', "error": form.errors}
    params = form.cleaned_data
    return {
        "status": 1,
        "apps": App.getRecentQuery(platform).fetch(params["count"], offset=params["offset"])
    }

def _detail_app(request, option = {}):
    app_id = long(option["app_id"])
    params = request.GET.copy()
    form = apiform.DetailAppForm(params)
    if not form.is_valid():
        return {"status": -1, "error": form.errors}
    params = form.cleaned_data
    app = App.get_by_id(app_id)
    if not app or app.status != 1:
        return {"status": -2, "error": "invalid app_id"}
    return {
        "status": 1,
        "app": app
    }
    


# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def _makeJson(request, do_method, option={}):
    '''
        do_methodを実行し、JSON/JSONP形式のレスポンスを含んだ
        HttpResponseオブジェクトを返す
        
        do_methodは
            requestを引数に取り
            JSONに変換可能なオブジェクトを返す
            関数である必要がある
    '''
    DOMAIN = "http://%s" %(request.META["SERVER_NAME"], )
    def to_json(obj):
        if isinstance(obj, ndb.Model):
            data = obj.to_dict()
            data["id"] = obj.key.id()
            if hasattr(obj, "created_at"):
                data["created_at"] = str(utils.jst_date(obj.created_at))[0:19]
            if hasattr(obj, "updated_at"):
                data["updated_at"] = str(utils.jst_date(obj.updated_at))[0:19]
            if hasattr(obj, "category"):
                data["category"] = arrays.get_category(obj.category)
            if hasattr(obj, "app_name"):
                data["app_image"]  = DOMAIN + reverse(app_icon, args=[str(obj.key.id()),])
                data["app_detail"] = DOMAIN + reverse(app_detail, args=[str(obj.key.id()),])
                data["app_id"] = data["id"]
            return data
    result = do_method(request, option)
    response = jsonDump(result, default=to_json)
    if not apiform.callbackform(request.REQUEST).is_valid():
        return HttpResponse(response)
    else :
        callback = request.REQUEST['callback']
        return HttpResponse("%s(%s);"%(callback, response))

''' 
 URL パターン
'''

urlpatterns = patterns(None,
    (r'^/app/recent/(\w+)/?$', recent_app),
    (r'^/app/detail/(\d+)/?$', detail_app),
    (r'^/developer/recent/?$', recent_developer),
    (r'^/?$', index),
)


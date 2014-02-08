#coding: utf-8

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.template import RequestContext
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
from app.models.developer import Developer
from app.models.app import App
from app import views
from app.libs.arrays import platforms
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

@custom_view
def index(request, context):
    context["developers"] = Developer.getQuery().fetch(10)
    context["recent_apps"] = {}
    for platform in platforms:
        apps = App.getRecentQuery(platform[0]).fetch(12)
        if apps:
            context["recent_apps"][platform[1]] = apps
    return render_to_response('webfront/index.html', context)

@custom_view
def about(request, context):
    context["current_tab"] = "about"
    return render_to_response('webfront/about.html',context)

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
    return render_to_response('webfront/developer_detail.html',context)

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
    return render_to_response('webfront/app_detail.html',context)   
    
# リリース前のみ利用するView
def pre(request):
    if request.method == 'POST':
        form = PreForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["user_mail"]
            user = PreUser.getByMail(email)
            user.put()
            _send_pre_complete_mail(email)
            return HttpResponseRedirect(reverse(pre_complete))
    else:
        form = PreForm()
    context = RequestContext(request, {
        "form": form,
    })
    return render_to_response('webfront/pre.html', context)

@cache_page(300)
def pre_complete(request):
    return render_to_response('webfront/pre_complete.html',{})
           

def _send_pre_complete_mail(email):
    message = mail.EmailMessage(
        sender=u"放課後アプリ部<info@houkago-no.appspotmail.com>",
        subject=u"事前登録が完了致しました。")
    message.to = email
    message.body = u"""この度は、放課後アプリ部の事前登録にご登録いただきありがとうございます。
サービスオープン時の事前登録が完了致しました。

http://houkago-no.appspot.com

現在、2014年1月を目処に開発を進めておりますので今しばらくお待ちください。
放課後アプリ部をどうぞよろしくお願いします。

※このメールアドレスは送信専用です。返信されても内容を確認できませんのでご注意ください。

============================
放課後アプリ部
http://houkago-no.appspot.com
============================
"""
    message.send()



#======================================================================================
''' 
 URL パターン
'''
urlpatterns = patterns(None,
    (r'^about/?$', about),
    (r'^pre_complete/?$', pre_complete),
    (r'^pre/?$', pre),
    (r'^user_id/(\d+)/?$' , user_id),
    (ur'^user/(\w+)/?$' , user),
    (r'^app_detail/(\d+)/?$' , app_detail),
    (r'^/?$', index),
)
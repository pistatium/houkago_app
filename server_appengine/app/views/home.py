#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
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
#from app.forms import registform
import syskey
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect


# -- Views  --------------------------------------------
# ------------------------------------------------------

def index(request):
    return render_to_response('webfront/index.html',{})

def demo(request):
    return render_to_response('webfront/demo.html',{})


# リリース前のみ
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
    (r'^demo/?$', demo),
    (r'^pre_complete/?$', pre_complete),
    (r'^pre/?$', pre),
    (r'^/?$', index),
)
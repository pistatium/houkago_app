#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from django.core.paginator import Paginator

from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.api import memcache
from google.appengine.api import mail

from hashlib import sha1, md5
from random import randint
from json import dumps as jsonDump
from datetime import datetime, timedelta
from logging import debug

# import from project
from common import models
from common import utils
from api import forms
import syskey
from django.views.decorators.cache import cache_page

# スレ立て連投規制時間
MAKE_THREAD_TIME = 3
# レス連投規制時間
MAKE_RES_TIME = 0.5



# -- Views  --------------------------------------------
# ------------------------------------------------------

def regist(request):
    ''' 端末登録 '''
    return _makeJson(request, _regist)

# Thread --------
def makeThread(request):
    ''' スレ立て '''
    return _makeJson(request, _makeThread)

@cache_page(10)
def getThread(request):
    ''' スレ一覧 '''
    return _makeJson(request, _getThread)


def evaluateThread(request):
    ''' スレ内レス一覧 '''
    return _makeJson(request, _evaluateThread)

# Res -----------
def makeRes(request):
    ''' レス作成 '''
    return _makeJson(request, _makeRes)

@cache_page(10)
def getRes(request):
    ''' スレ内一覧 '''
    return _makeJson(request, _getRes)

def evaluateRes(request):
    ''' レスいいね '''
    return _makeJson(request, _evaluateRes)

def deleteRes(request):
    ''' レス削除 '''
    return _makeJson(request, _deleteRes)

def deleteThread(request):
    ''' レス削除 '''
    return _makeJson(request, _deleteThread)

def notfound(request):
    raise Http404


# -- Private Methods -----------------------------------
# ------------------------------------------------------

def _regist(request):
    '''
        regist view の本体
    '''
    debug('regist');
    form = forms.RegistForm(request.POST)
    if not form.is_valid():
        return {"status": -1, "device_id": request.REQUEST.get("device_id","")}
    params = form.cleaned_data
    
    device_id    = params['device_id']
    device_hash  = params['device_hash']
    
    if not _checkHash(device_id, device_hash):
        return {"status":-2}

    user = models.UserModel.get(device_id)
    # 
    if user:
       return  {"status":-3, "device_key": user.device_key}
    else:
        user = models.UserModel()
    device_key = _createKey()
    result = user.registNewDevice(device_id, device_key)
    if result:
        return {"status":1, "device_key": device_key}
    else:
        return {"status":1, "device_key":''}


def _makeThread(request):
    '''
        makeThread view の本体
    '''
    params = request.POST.copy()
    form = forms.makeThreadForm(params)
    if not form.is_valid():
        return {"status": -1, "thread_id":'', "error": form.errors}
    params = form.cleaned_data

    user = models.UserModel.get(params["device_id"])
    if not _checkToken(params, user):
        return {"status": -2, "thread_id":''}
    
    # 連投チェック
    if user.last_action:
      if datetime.now() - user.last_action < timedelta(0, MAKE_THREAD_TIME * 60):
        return {"status": -5, "thread_id":''}

    #星はadmin専用にする
    params["uname"] = _change_uname(params["uname"])

    try:
      # スレ作成
      thread = models.ThreadModel.create(params)
      params['thread_id'] = thread.key.id()
      # >>1作成
      res    = models.ResModel.create(params, 0)
      # スレと>>1紐付け
      thread.insertResOneId(res.key.id())
      user.doneAction()
    
    except Exception, e:
      return e
      debug(e)
      # 失敗したら削除
      if thread:
          thread.delete()
      if res:
          res.delete()
      return {"status": -3, "rhread_id":''}
    return {"status": 1, "rhread_id": thread.key.id()}


def _getThread(request):
    '''
        getThread view の本体
    '''
    params = request.GET.copy()
    form = forms.getThreadForm(params)
    if not form.is_valid():
        return {"status": -1, "error": form.errors}
    params = form.cleaned_data
    
    thread = models.ThreadModel.get(params)
    return { "status": 1,
             "data"  : {
                 "thread": thread.object_list,
                 "has_next": thread.has_next(),
                 "has_previous": thread.has_previous(),
             },
           }

def _evaluateThread(request):

    params = request.POST.copy()
    form = forms.evaluateThreadForm(params)
    if not form.is_valid():
        return {"status": -1}
    params = form.cleaned_data
    
    user = models.UserModel.get(params["device_id"])
    if not _checkToken(params, user):
        return {"status": -2}

    thread = models.ThreadModel.evaluate(
        int(params["thread_id"]),
        user.key.id(),
        int(params["is_plus"])
    )
    if not thread:
        return {"status": -4}
    
    if len(thread.minused_user) > 2:
        reportMail(thread.key.id())

    return { "status": 1,
             "plus_count": len(thread.plused_user)}


def _makeRes(request):
    '''
        makeRes view の本体
    '''
    params = request.POST.copy()
    form = forms.makeResForm(params)
    if not form.is_valid():
        return {"status": -1, "thread_res_id":'', "res_id": '', "error": form.errors}
    params = form.cleaned_data
    
    user = models.UserModel.get(params["device_id"])
    if not _checkToken(params, user):
        return {"status": -2, "thread_res_id":'', "res_id": ''}

    #星はadmin専用にする
    params["uname"] = _change_uname(params["uname"])
    
    # 連投チェック
    if user.last_action:
      if datetime.now() - user.last_action < timedelta(0, MAKE_RES_TIME * 60):
        return {"status": -5, "thread_id":''}
    res = None
    try:
        
        res = models.ResModel.create(params);
        if res is None:
            return {"status": -4, "thread_res_id":'', "res_id": ''}
        models.ThreadModel.addRes(int(params["thread_id"]))
        user.doneAction()
    except:
        if res.key:
            res.key.delete()
        return {"status": -3, "thread_res_id":'', "res_id": ''}
    return {"status": 1, "thread_res_id": res.number, "res_id": res.key.id()}


def _change_uname(uname):
    uname = uname.replace(u"★","[]").replace(u"☆","[]")
    uname = uname.replace(u"◆","[]").replace(u"◇","[]")
    uname = uname.replace(u"k@m@tte",u"かまってch運営★")
    return uname
    
def _evaluateRes(request):
    params = request.POST.copy()
    form = forms.evaluateResForm(params)
    if not form.is_valid():
        return {"status": -1}
    params = form.cleaned_data
    
    user = models.UserModel.get(params["device_id"])
    if not _checkToken(params, user):
        return {"status": -2}
    
    res = models.ResModel.evaluate(
        int(params["res_id"]),
        user.key.id(),
        int(params["is_plus"])
    )
    if not res:
        return {"status": -4}

    if len(res.minused_user) > 2:
        reportMail(res.key.id())

    return { "status": 1,
             "plus_count": len(res.plused_user),
             "minus_count": len(res.minused_user)
            }

    
def _getRes(request):
    '''
        getRes view の本体
    '''
    params = request.GET.copy()
    form = forms.getResForm(params)
    if not form.is_valid():
        return {"status": -1, "error": form.errors}
    params = form.cleaned_data
    try:
        thread = models.ThreadModel.get_by_id(int(params['thread_id']));
    except BadRequestError:
        return {"status": -1, "error": "There is no thread such id"}
    
    res = models.ResModel.getByThreadId(params)
    return { "status": 1,
             "data": {
                 "res": res.object_list,
                 "has_next": res.has_next(),
                 "has_previous": res.has_previous(),
                 "thread": thread,
             },
            }

def _deleteRes(request):
    '''
        deleteRes view の本体
    '''
    params = request.POST.copy()
    form = forms.deleteResForm(params)
    if not form.is_valid():
        return {"status": -1, "error": form.errors}
    params = form.cleaned_data
    
    user = models.UserModel.get(params["device_id"])
    if not _checkToken(params, user):
        return {"status": -2}
    try:
        res = models.ResModel.get_by_id(params["res_id"])
        res.donadona()
        return {"status": -1}
    except:
        return {"status": -9}
        
def _deleteThread(request):
    '''
        deleteRes view の本体
    '''
    params = request.POST.copy()
    form = forms.deleteThreadForm(params)
    if not form.is_valid():
        return {"status": -1, "error": form.errors}
    params = form.cleaned_data
    
    user = models.UserModel.get(params["device_id"])
    if not _checkToken(params, user):
        return {"status": -2}

    try:
        thread = models.ThreadModel.get_by_id(params["thread_id"])
        thread.key.delete()
        return {"status": 1}
    except:
        return {"status": -9}    
## ------------------------------------------------------

def _makeJson(request, do_method):
    '''
        do_methodを実行し、JSON/JSONP形式のレスポンスを含んだ
        HttpResponseオブジェクトを返す
        
        do_methodは
            requestを引数に取り
            JSONに変換可能なオブジェクトを返す
            関数である必要がある
    '''
    def to_json(obj):
        if isinstance(obj, ndb.Model):
            data = obj.to_dict()
            data["id"] = obj.key.id()
            if hasattr(obj, "uname"):
                data["uname"] = _changeTrip(data["uname"])
            if hasattr(obj, "created_at"):
              data["created_at"] = str(utils.jst_date(obj.created_at))[0:19]
            if hasattr(obj, "updated_at"):
              data["updated_at"] = str(utils.jst_date(obj.updated_at))[0:19]
            if hasattr(obj, "user_id"):
              if data["uname"] and data["uname"].count(u'★'):
                data["user_hash"]  = _makeUserHash(data["user_id"], obj.created_at, True)
              else:
                data["user_hash"]  = _makeUserHash(data["user_id"], obj.created_at)
              del(data["user_id"])
            if hasattr(obj, "plused_user"):
              data["plus_num"] = len(obj.plused_user)
              del(data["plused_user"])
            if hasattr(obj, "minused_user"):
              data["minus_num"] = len(obj.minused_user)
              del(data["minused_user"])
              
            return data
        
    result = do_method(request)
    response = jsonDump(result, default=to_json)
    if not forms.CallbackForm(request.REQUEST).is_valid():
        return HttpResponse(response)
    else :
        callback = request.REQUEST['callback']
        return HttpResponse("%s(%s);"%(callback, response))
    
##  Utils ----------------------------------------------------
## -----------------------------------------------------------

def reportMail(res_id):
   memkey = "res_id:" + str(res_id)
   is_send = memcache.get(memkey)
   if is_send is not None:
       return

   message = mail.EmailMessage(sender="Kamatte Report System <delete@kamatte-ch.appspotmail.com>",
                               subject="Confirm delete request") 
   message.to = "info@kamatte.ch"
   message.body = """
     %d is requested for delete.

     if delete this res, click here.
     http://
   """% (res_id)
   message.send()
   memcache.add(memkey, "sended", 60 * 60)

def _hexTo64(hex):
    result = []
    for i in range(10):
        # 16 * 16 / 4 = 64
        tmp = int(hex[i * 2: i * 2 + 2],16) / 4
        if tmp < 26:
            # A-Z
            result.append(chr(tmp + 65))
        elif 26 <= tmp < 52:
            # a-z
            result.append(chr(tmp - 27 + 97))
        elif tmp == 52:
            result.append('_')
        elif tmp == 53:
            result.append('+')
        else:
          result.append(str(tmp - 54))
    return ''.join(result)

def _hexToHira(hex):
    result = []
    for i in range(8):
        # 16 * 16 / 4 = 64
        tmp = int(hex[i * 2: i * 2 + 2],16) / 4
        HIRAGANA = list(u'あいうえおかきくけこさしすせそたちっつてとなにぬねのはひふへほまみむめもやゆよらりるれろわんをあいうえおあいうえおのののののののの')
        result.append(HIRAGANA[tmp])
    return ''.join(result)
    
def _changeTrip(user_name):
    sharp_pos = user_name.find(u'#')
    if sharp_pos == -1:
        return user_name
    else:
        seed = user_name[sharp_pos:]
        return user_name[:sharp_pos] + u"◆" + _hexTo64(md5(seed.encode('utf=8')).hexdigest())
        
def _checkHash(d_id, d_hash):
    debug("checkHash\n  d_hash" + d_hash)
    return _createHash(d_id) == d_hash

def _createHash(d_id):
    seed = syskey.device_key_pre + d_id + syskey.device_key_post
    debug("createHash\n  seed: " + seed)
    c_hash = sha1(seed).hexdigest()
    debug("createHash\n c_seed: " + c_hash)
    return c_hash

def _checkToken(params, user):
    if not user:
        return False
    token = _makeToken(user.device_key)
    return bool(params["token"] == token)
    
def _createKey():
    return "".join([chr(randint(98,121)) for i in range(64)])

def _makeToken(key):
    d = datetime.today()
    seed = key + utils.jst_date().strftime("%Y%m%d") + syskey.token_key
    debug("makeToken\n  seed: " + seed)
    return sha1(seed).hexdigest()

def _makeUserHash(userid, created_at, is_admin = False):
    if is_admin:
        userid += "_admin"
    seed = str(userid) + "@" + utils.jst_date(created_at).strftime("%Y%m%d")
    return _hexTo64(md5(seed).hexdigest())

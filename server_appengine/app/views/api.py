#coding: utf-8
from app.libs import utils

@utils.login_required
def img_upload(request):
    return _makeJson(request, _img_upload)


def _img_upload(request):
    user = users.get_current_user()
    
    photo = request.get("photo")



# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
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

import datetime
from hashlib import sha1
from django.http import HttpResponseRedirect
from google.appengine.api import users
from syskey import api_key

class UtcTzinfo(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def olsen_name(self):
        return 'UTC'

class JstTzinfo(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=9)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'JST'

    def olsen_name(self):
        return 'Asia/Tokyo'

def make_api_key(value):
    seed = (api_key % (value))
    return sha1(seed).hexdigest()

def jst_date(value=''):
    if not value:
        value = datetime.datetime.now()

    value = value.replace(tzinfo=UtcTzinfo()).astimezone(JstTzinfo())
    return value


def login_required(fn):
    """ checks to see if the user is logged in, if not, redirect to login """

    def _dec(view_func):
        def _checklogin(request, *args, **kwargs):

            user = users.get_current_user()
            if user:
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponseRedirect(users.create_login_url(request.get_full_path()))
                
        _checklogin.__doc__ = view_func.__doc__

        _checklogin.__dict__ = view_func.__dict__

        return _checklogin

    return _dec(fn)

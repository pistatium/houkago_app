import datetime
import time
from hashlib import sha1
from django.http import HttpResponseRedirect
from google.appengine.api import users
from syskey import api_key
from hashlib import sha1

from django.core.cache import cache as _djcache

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

def timestamp(dt):
    dt = jst_date(dt)
    return time.mktime(dt.timetuple())

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



# https://djangosnippets.org/snippets/564/
def cache(seconds = 900):
    """
        Cache the result of a function call for the specified number of seconds, 
        using Django's caching mechanism.
        Assumes that the function never returns None (as the cache returns None to indicate a miss), and that the function's result only depends on its parameters.
        Note that the ordering of parameters is important. e.g. myFunction(x = 1, y = 2), myFunction(y = 2, x = 1), and myFunction(1,2) will each be cached separately. 

        Usage:

        @cache(600)
        def myExpensiveMethod(parm1, parm2, parm3):
            ....
            return expensiveResult
`
    """
    def doCache(f):
        def x(*args, **kwargs):
                key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
                result = _djcache.get(key)
                if result is None:
                    result = f(*args, **kwargs)
                    _djcache.set(key, result, seconds)
                return result
        return x
    return doCache

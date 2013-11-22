#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from django.core.paginator import Paginator

from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadRequestError
from google.appengine.api import memcache
from google.appengine.api import users

from hashlib import sha1, md5
from random import randint
from datetime import datetime, timedelta
from logging import debug

# import from project
from common import models
from common import utils
from webfront import forms
import syskey
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect


# -- Views  --------------------------------------------
# ------------------------------------------------------

def index(request):
    return render_to_response('webfront/index.html',{})


def notfound(request):
    raise Http404
           
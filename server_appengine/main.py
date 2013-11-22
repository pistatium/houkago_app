import os
import sys
import logging

# Google App Engine imports.
#from google.appengine.ext.webapp import util

import django.core.handlers.wsgi
from google.appengine.api import memcache

import settings
import django.conf

sys.modules['memcache'] = memcache

'''
  load setting file
  http://stackoverflow.com/questions/5122414/django-googleappengine-error-django-settings-module-is-undefined
'''
# Filter out all the non-setting attributes of the settings module
settingsKeys = filter(lambda name: str(name) == str(name).upper(), 
                      dir(settings))

# copy all the setting values from the settings module into a dictionary
settingsDict = dict(map(lambda name: (name, getattr(settings, name)), 
                        settingsKeys))

django.conf.settings.configure(**settingsDict)

# faile
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

django_app = django.core.handlers.wsgi.WSGIHandler()

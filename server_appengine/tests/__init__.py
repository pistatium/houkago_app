# coding: utf-8

from __future__ import absolute_import, division, print_function

import django.conf

from .. import settings

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

settingsDict.update({
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
})
django.conf.settings.configure(**settingsDict)

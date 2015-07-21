# coding: utf-8
from __future__ import absolute_import, division, print_function

from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.conf.urls import patterns

from app.models.app import App
from app import views

# -- Views  --------------------------------------------
# ------------------------------------------------------


@cache_page(60 * 5)
def to_home(request, app_id):
    app = App.getById(int(app_id))
    if app:
        app.affiriate_point_total += 2
        app.affiriate_point += 2
        app.put()
    return HttpResponseRedirect(reverse(views.home.index))


@cache_page(60 * 5)
def to_app(request, app_id):
    app = App.getById(int(app_id))
    if app:
        app.affiriate_point_total += 1
        app.affiriate_point += 1
        app.put()
    return HttpResponseRedirect(reverse(views.home.app_detail, args=[app_id]))


# ======================================================================================

'''
 URL パターン
'''
urlpatterns = patterns(None,
        (r'^/to_home/(\d+)/?$', to_home),
        (r'^/to_app/(\d+)/?$', to_app),

)

# coding: utf-8
from __future__ import absolute_import, division, print_function

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.conf.urls import patterns
from google.appengine.api import users
from django.template import RequestContext

from app.libs import utils
from app.models.appc import AppC
from app import views

# -- Views  --------------------------------------------
# ------------------------------------------------------


def admin_view(view):
    import functools

    @functools.wraps(view)
    @utils.login_required
    def override_view(*args, **kwargs):
        request = args[0]
        user = users.get_current_user()
        if not user or not users.is_current_user_admin():
            raise Http404
        kwargs["context"] = RequestContext(request)
        return view(*args, **kwargs)
    return override_view

@admin_view
def appc(request, page=0, context={}):
    if request.method == 'POST':
        codes = request.POST["serials"].splitlines()
        AppC.batch_import(codes)
        context["codes"] = codes
    page = int(page)
    context["codes"] = AppC.get_list(page)
    context["page"] = page
    return render_to_response('admin/appc.html', context)

# ======================================================================================

'''
 URL パターン
'''
urlpatterns = patterns(None,
    (r'^/appc/$', appc),
    (r'^/appc/(\d+)?$', appc),
)

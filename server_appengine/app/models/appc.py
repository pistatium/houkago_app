# coding: utf-8

from __future__ import absolute_import, division, print_function

from google.appengine.ext import ndb


class AppC(ndb.Model):
    grant_user = ndb.IntegerProperty()
    serial = ndb.StringProperty()
    status = ndb.IntegerProperty(default=0)  # 1 配布済
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def grant(cls, developer_id):
        codes = cls.query(cls.grant_user == developer_id).fetch(1)
        if codes:
            return codes[0]
        codes = cls.query(cls.status == 0).fetch(1)
        if not codes:
            return None
        code = codes[0]
        code.grant_user = developer_id
        code.status = 1
        code.put()
        return code

    @classmethod
    def batch_import(cls, serials):
        codes = []
        for serial in serials:
            # insert uniq
            appc_key = ndb.Key(cls, serial)
            codes.append(AppC(serial=serial, key=appc_key))
        ndb.put_multi(codes)

    @classmethod
    def get_list(cls, page=0):
        COUNT = 100
        offset = page * COUNT
        return cls.query().order(cls.status).fetch(COUNT, offset=offset)

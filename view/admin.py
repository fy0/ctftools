# coding:utf-8

import json
import zlib
import base64
import config
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView


@route('/j/admin/close_reg', name='j_close_reg')
class Admin(AjaxLoginView):
    def post(self):
        config.ALLOW_REG = False
        self.finish({"code":0})


@route('/j/admin/open_reg', name='j_open_reg')
class Admin(AjaxLoginView):
    def post(self):
        config.ALLOW_REG = True
        self.finish({"code":0})


@route('/j/admin/spec_save', name='j_admin_spec_save')
class Admin(AjaxLoginView):
    def post(self):
        SERV_HOST = self.get_argument('SERV_HOST')
        config.SPEC['SERV_HOST'] = SERV_HOST
        config.spec_save()
        self.finish({"code":0})

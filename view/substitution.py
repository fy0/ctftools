# coding:utf-8

import json
import zlib
import base64

from lib.cipher_solve import decrypt
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView


@route('/j/subsitution', name='substitution')
class OneLine(AjaxLoginView):
    def post(self):
        txt = self.get_argument('txt', '')
        ret = decrypt.decrypt(txt)
        self.finish(json.dumps({
            "msg": ret,
        }))

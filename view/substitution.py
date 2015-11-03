# coding:utf-8

import json
import zlib
import base64
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView

@route('/j/subsitution', name='j_substitution')
class OneLine(AjaxLoginView):
    def post(self):
        txt = self.get_argument('txt', '')

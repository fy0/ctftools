# coding:utf-8

import json
import zlib
import base64
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView

xss_info = []


@route('/x', name='j_xss')
class OneLine(AjaxView):
    def get(self):
        #print(self.request.headers)
        txt = self.get_argument('c', '')
        print(txt)
        xss_info.append([self.request.headers.get("Referer"), txt])

    post = get


@route('/xss/ret', name='xss_ret')
class OneLine(LoginView):
    def get(self):
        ret = ''
        for i in xss_info:
            ret += ("<li><p>referer: %s</p>%s</li>\n" % (i[0], i[1]))
        self.write(ret)
        self.finish()

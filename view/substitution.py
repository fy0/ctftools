# coding:utf-8

import json
import zlib
import base64
import time
from tornado.gen import coroutine
from tornado.web import asynchronous
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from lib.cipher_solve import decrypt
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView


@route('/j/subsitution', name='substitution')
class Substitution(AjaxLoginView):
    executor = ThreadPoolExecutor(30)

    @coroutine
    @asynchronous
    def post(self):
        txt = self.get_argument('txt', '')
        before = time.time()
        ret = yield self.work(txt)
        self.finish(json.dumps({
            "msg": ret,
        }))

    @run_on_executor
    def work(self, txt):
        ret = decrypt.decrypt(txt)
        return ret

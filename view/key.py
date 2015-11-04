# coding:utf-8

import json
import zlib
import base64
import time
from model.flag_log import FlagLog
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView


@route('/k', name='j_key')
class KeyView(AjaxView):
    def get(self):
        c = self.get_argument('c', '')
        try:
            key = str(zlib.decompress(base64.b64decode(c)), 'utf-8')
        except:
            key = None
        if key:
            print(key)
            FlagLog.new(self.request.remote_ip, int(time.time()), key)

    post = get


@route('/j/flag_info', name='j_flag_info')
class FlagInfo(AjaxLoginView):
    last_recent = []

    @classmethod
    def in_info(cls, ip, info):
        for i in info:
            if ip == i['ip']:
                return True
        return

    def get(self):
        recent = list(FlagLog.get_recent())

        # 上次在而这次不在，失去的主机
        lost_lst = []
        for i in FlagInfo.last_recent:
            if not self.in_info(i['ip'], recent):
                lost_lst.append(i)

        # 这次新增的主机
        new_lst = []
        for i in recent:
            if not self.in_info(i['ip'], FlagInfo.last_recent):
                new_lst.append(i)

        FlagInfo.last_recent = recent
        self.finish(json.dumps({"lost": lost_lst, "new": new_lst, "recent": recent}))

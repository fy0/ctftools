# coding:utf-8

import json
import config
from model.chat_log import ChatLog
from model.user import User
from view import route, url_for, View
from tornado.web import decode_signed_value
from sockjs.tornado import SockJSRouter, SockJSConnection


class ChatConnection(SockJSConnection):
    visitors = set()

    def on_open(self, request):
        self.user = None
        try:
            value = json.loads(request.cookies['u'].coded_value)
        except KeyError:
            self.broadcast([self], json.dumps([['connect_ret', {'code': -1}]]))
            return False

        key = decode_signed_value(config.COOKIE_SECRET, 'u', value, max_age_days=31, min_version=None)
        user = User.get_by_key(key)
        if user is None:
            self.broadcast([self], json.dumps([['connect_ret', {'code': -1}]]))
            return False

        self.user = user
        self.broadcast([self], json.dumps([
            ['connect_ret', {'code': 0, 'username':user.username, "msg_log":ChatLog.get_list()}]
        ]))
        self.visitors.add(self)

    def on_close(self):
        self.visitors.remove(self)

    def say(self, txt, to_user=None):
        cl = ChatLog.new(self.user, txt, to_user)
        self.broadcast(self.visitors, json.dumps([
           ['say_ret', {"user_id": self.user.id, "username":self.user.username, "time": cl.time_human(), "txt":txt}],
        ]))

    def on_message(self, message):
        if self.user is None:
            return
        info = json.loads(message)

        for i in info:
            key = i[0]
            if key == 'say':
                self.say(i[1])

chat_route = SockJSRouter(ChatConnection, '/ws/api')

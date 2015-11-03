# coding:utf-8

from peewee import *
import time
import datetime
from model import BaseModel
from model.user import User


class ChatLog(BaseModel):
    user = ForeignKeyField(User, null=True)
    to_user = ForeignKeyField(User, related_name="send_to_user_id", null=True)
    time = BigIntegerField(index=True)
    txt = CharField(max_length=10240, null=True)

    @classmethod
    def new(cls, user, txt, to_user=None):
        return cls.create(user=user, to_user=to_user, txt=txt, time=int(time.time()))

    def time_human(self):
        return datetime.datetime.fromtimestamp(self.time).strftime('%Y-%M-%d %H:%M:%S')

    @classmethod
    def get_list(cls):
        ret = []
        for i in cls.select():
            info = {
                'user_id': i.user.id,
                'username': i.user.username,
                'time': i.time_human(),
                'txt': i.txt,
            }
            ret.append(info)
        return ret

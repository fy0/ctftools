# coding:utf-8
# 远端发回的flag数据

from peewee import *
import time
import datetime
from model import BaseModel
from model.user import User


class FlagLog(BaseModel):
    ip = TextField(index=True)
    time = BigIntegerField(index=True)
    key = CharField(max_length=1024, null=True)

    @classmethod
    def new(cls, ip, time, key):
        return cls.create(ip=ip, time=time, key=key)

    def time_human(self):
        return datetime.datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "ip": self.ip,
            "time": self.time_human(),
            "key": self.key,
        }

    @classmethod
    def in_info(cls, ip, info):
        for i in info:
            if ip == i['ip']:
                return True
        return

    @classmethod
    def get_recent(cls):
        ret = []
        cur = time.time()
        for i in cls.select().where(cls.time > cur - 60*3).order_by(cls.time.desc()):
            if cls.in_info(i.ip, ret):
                continue
            info = i.to_dict()
            offset = cur - i.time
            if 0 <= offset <= 60:
                info['tip'] = '一分钟内'
            elif 60 <= offset <= 60*2:
                info['tip'] = '两分钟内'
            elif 60*2 <= offset <= 60*3:
                info['tip'] = '三分钟内'
            ret.append(info)
        return ret

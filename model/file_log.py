# coding:utf-8

import time
import datetime
from peewee import *
from model import BaseModel
from model.user import User


class FileLog(BaseModel):
    filename = TextField(index=True)
    original_filename = TextField(index=True)
    user = ForeignKeyField(User, null=True)
    time = BigIntegerField(index=True)
    txt = CharField(max_length=1024, null=True)

    @classmethod
    def new(cls, filename, original_filename, user, txt=""):
        return cls.create(filename=filename, original_filename=original_filename, user=user, txt=txt, time=int(time.time()))

    def time_human(self):
        return datetime.datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            'filename': self.filename,
            'original_filename': self.original_filename,
            'user_id': self.user.id,
            'username': self.user.username,
            'time': self.time_human(),
            'txt': self.txt,
        }

    @classmethod
    def get_list(cls):
        ret = []
        for i in cls.select():
            ret.append(i.to_dict())
        return ret

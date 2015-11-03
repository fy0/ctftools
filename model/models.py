# coding:utf-8

from model import db
from model.test import Test
from model.user import User
from model.chat_log import ChatLog

db.connect()
db.create_tables([Test, User, ChatLog], safe=True)

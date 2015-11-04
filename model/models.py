# coding:utf-8

from model import db
from model.test import Test
from model.user import User
from model.chat_log import ChatLog
from model.file_log import FileLog
from model.flag_log import FlagLog

db.connect()
db.create_tables([Test, User, ChatLog, FileLog, FlagLog], safe=True)

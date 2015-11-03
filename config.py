# coding:utf-8

PORT = 9000
DEBUG = True
TITLE = 'ctftool'
TEMPLATE = 'mako'  # jinja2/mako/tornado
DATABASE_URI = "sqlite:///database.db"
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"
ALLOW_REG = True

try:
    from private import *
except:
    pass

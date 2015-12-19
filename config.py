# coding:utf-8
import json

PORT = 8081
DEBUG = True
TITLE = 'ctftool'
TEMPLATE = 'mako'  # jinja2/mako/tornado
DATABASE_URI = "sqlite:///database.db"
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"
ALLOW_REG = True

SPEC = {
    "SERV_HOST": '192.168.30.102'
}


def spec_save():
    open('spec.json', 'w', encoding='utf-8').write(json.dumps(SPEC))


def spec_load():
    global SPEC
    SPEC = json.loads(open('spec.json', 'r', encoding='utf-8').read())

try:
    spec_load()
except:
    pass

try:
    from private import *
except:
    pass

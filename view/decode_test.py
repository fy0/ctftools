# coding:utf-8

import re
import base64
import hashlib
import json
import binascii
from urllib.parse import quote, unquote
from view import route, url_for, View, LoginView, AjaxLoginView


def str_in(s):
    return s.encode('utf-8')


def str_out(s):
    return str(s, 'utf-8')


@route('/j/decode_test', name='j_decode_test')
class DecodeSource(AjaxLoginView):
    def compute(self, src):
        try: base64_out = str_out(base64.b64decode(str_in(src)))
        except: base64_out = '无法解析'

        try: hex_out = str_out(binascii.unhexlify(str_in(src)))
        except: hex_out = '无法解析'

        try: hex2_out = str(binascii.unhexlify(src.replace(' ', '').replace('0x', '')), 'utf-8')
        except: hex2_out = '无法解析'

        try: utf7_out = str(src.encode('utf-8'), 'utf-7')
        except: utf7_out = '无法解析'

        try: quote_out = unquote(src)
        except: quote_out = '无法解析'

        return {
            "source": src,
            "base64": base64_out,
            "hex": hex_out,
            "hex2": hex2_out,
            "utf7": utf7_out,
            'quote': quote_out,
            "code": 0,
        }

    def post(self):
        src = self.get_argument('source', '')
        if src:
            self.finish(json.dumps(self.compute(src)))
        else:
            self.finish({"code": -1})

# coding:utf-8

import re
import base64
import hashlib
import json
import binascii
from urllib.parse import quote, unquote
from view import route, url_for, View, LoginView, AjaxLoginView

MOS_CODE = {
    'A': '.-',     'B': '-...',   'C': '-.-.',
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',

    '0': '-----',  '1': '.----',  '2': '..---',
    '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.'
}

MOS_CODE_REV = {}

for k, v in MOS_CODE.items():
    MOS_CODE_REV[v] = k


def mos_encode(s):
    ret = []
    for i in s.upper():
        ret.append(MOS_CODE.get(i) or '?')
    return ''.join(ret)


'''def mos_decode(s):
    ret = []
    while s:
        find = False
        for k, v in MOS_CODE.items():
            if s.startswith(v):
                ret.append(k)
                find = True
                s = s[len(v):]
                break
        if not find:
            ret.append('?')
            break
    return ''.join(ret)'''


def str_in(s):
    return s.encode('utf-8')


def str_out(s):
    return str(s, 'utf-8')


class DecodeView(AjaxLoginView):
    def compute(self, src):
        return {
            "source": src,
            "base64": str_out(base64.b64encode(str_in(src))),
            "hex": str_out(binascii.hexlify(str_in(src))),
            "hex2": re.sub(r'(..)', r'0x\1 ', str_out(binascii.hexlify(str_in(src)))),
            "utf7": str_out(src.encode('utf-7')),
            'quote': quote(src),
            'morse': mos_encode(src),
            "md5": hashlib.md5(str_in(src)).hexdigest(),
            "code": 0,
        }


@route('/j/decode/source', name='j_decode_source')
class DecodeSource(DecodeView):
    def post(self):
        src = self.get_argument('source', '')
        if src:
            self.finish(json.dumps(self.compute(src)))
        else:
            self.finish({"code": -1})


@route('/j/decode/base64', name='j_decode_base64')
class DecodeSource(DecodeView):
    def post(self):
        b64 = self.get_argument('base64', '')
        try:
            src = str(base64.b64decode(b64), 'utf-8')
        except:
            src = None
        if src:
            ret = self.compute(src)
            ret["base64"] = b64
            self.finish(json.dumps(ret))
        else:
            self.finish({"code": -1})


@route('/j/decode/hex', name='j_decode_hex')
class DecodeSource(DecodeView):
    def post(self):
        hex = self.get_argument('hex', '')
        try:
            src = str(binascii.unhexlify(hex), 'utf-8')
        except:
            src = None
        if src:
            ret = self.compute(src)
            ret["hex"] = hex
            self.finish(json.dumps(ret))
        else:
            self.finish({"code": -1})


@route('/j/decode/hex2', name='j_decode_hex2')
class DecodeSource(DecodeView):
    def post(self):
        hex = self.get_argument('hex2', '')
        try:
            src = str(binascii.unhexlify(hex.replace('0x ', '')), 'utf-8')
        except:
            src = None
        if src:
            ret = self.compute(src)
            ret["hex2"] = hex
            self.finish(json.dumps(ret))
        else:
            self.finish({"code": -1})


@route('/j/decode/utf7', name='j_decode_utf7')
class DecodeSource(DecodeView):
    def post(self):
        u7 = self.get_argument('utf7', '')
        try:
            src = str(bytes(u7, 'utf-8'), 'utf-7')
        except:
            src = None
        if src:
            ret = self.compute(src)
            ret["utf7"] = u7
            self.finish(json.dumps(ret))
        else:
            self.finish({"code": -1})


@route('/j/decode/quote', name='j_decode_quote')
class DecodeSource(DecodeView):
    def post(self):
        quote = self.get_argument('quote', '')
        try:
            src = unquote(quote)
        except:
            src = None
        if src:
            ret = self.compute(src)
            ret["quote"] = quote
            self.finish(json.dumps(ret))
        else:
            self.finish({"code": -1})

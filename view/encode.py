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
    return '/'.join(ret)


def mos_decode(s):
    ret = []
    for i in s.split('/'):
        chr = MOS_CODE_REV.get(i)
        if chr == None: chr = '?'
        ret.append(chr)
    return ''.join(ret)


def str_in(s):
    return s.encode('utf-8')


def str_out(s):
    return str(s, 'utf-8')


class EncodeView(AjaxLoginView):
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


@route('/j/encode/source', name='j_encode_source')
class EncodeSource(EncodeView):
    def post(self):
        src = self.get_argument('source', '')
        if src:
            self.finish(json.dumps(self.compute(src)))
        else:
            self.finish({"code": -1})


@route('/j/encode/base64', name='j_encode_base64')
class EncodeSource(EncodeView):
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


@route('/j/encode/hex', name='j_encode_hex')
class EncodeSource(EncodeView):
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


@route('/j/encode/hex2', name='j_encode_hex2')
class EncodeSource(EncodeView):
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


@route('/j/encode/utf7', name='j_encode_utf7')
class EncodeSource(EncodeView):
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


@route('/j/encode/quote', name='j_encode_quote')
class EncodeSource(EncodeView):
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


@route('/j/encode/morse', name='j_encode_morse')
class EncodeSource(EncodeView):
    def post(self):
        val = self.get_argument('morse', '')
        try:
            src = mos_decode(val)
        except:
            src = None
        if src:
            ret = self.compute(src)
            ret["morse"] = val
            self.finish(json.dumps(ret))
        else:
            self.finish({"code": -1})

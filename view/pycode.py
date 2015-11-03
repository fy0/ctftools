# coding:utf-8

import json
import zlib
import base64
from view import route, url_for, View, LoginView, AjaxLoginView


def code_pack_py2(txt):
    r = str(base64.b64encode(zlib.compress(txt.encode('utf-8'))), 'utf-8')
    return '''#!/usr/bin/python
import zlib, base64
exec(compile(zlib.decompress(base64.b64decode('%s')), '', 'exec'))''' % r

def get_one_line(txt):
    return 'python -c "%s"\n' % ';'.join(txt.split('\n')[1:])


@route('/j/pycode', name='j_pycode')
class OneLine(AjaxLoginView):
    def post(self):
        txt = self.get_argument('txt', '')

        pack = code_pack_py2(txt)
        one_line = get_one_line(pack)

        self.finish(json.dumps({
            "pack": pack,
            "one_line": one_line,
        }))

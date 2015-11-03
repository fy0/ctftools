# coding:utf-8

import json
import os
import random
import string
from model.file_log import FileLog
from view import route, url_for, View, LoginView, AjaxLoginView, AjaxView


@route('/j/upload', name='j_upload')
class UploadHandler(AjaxLoginView):
    def post(self):
        file1 = self.request.files['file'][0]
        original_fname = file1['filename']
        extension = os.path.splitext(original_fname)[1]
        fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(24))
        final_filename = fname + extension
        output_file = open("static/uploads/" + final_filename, 'wb')
        output_file.write(file1['body'])
        fl = FileLog.new(final_filename, original_fname, self.current_user())
        self.finish(json.dumps(fl.to_dict()))


@route('/j/upload_file_lst', name='j_upload_file_lst')
class UploadHandler(AjaxLoginView):
    def post(self):
        self.finish(json.dumps(FileLog.get_list()))

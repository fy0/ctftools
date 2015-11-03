# coding:utf-8

from view import route, url_for, View, LoginView


@route('/', name='index')
class Index(LoginView):
    def get(self):
        self.render()


@route('/jump_test', name='jump')
class Jump(View):
    def get(self):
        self.messages.error('Message Test: Error!!中文测试!!')
        self.redirect(url_for('about'))


@route('/about', name='about')
class About(View):
    def get(self):
        self.render()

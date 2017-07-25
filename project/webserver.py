# -*- coding: utf-8 -*-

import tornado.web
import logging
import os
import re

import project.database


#-----------------------------------------------------------------------------
# WEB SERVER
#-----------------------------------------------------------------------------

class EndpointHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('endpoint.html', data=None)

    def post(self):
        arg1 = self.get_body_argument('arg1')
        arg2 = self.get_body_argument('arg2')
        data = project.database.find(arg1, arg2)

        self.render('endpoint.html', data=data)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


app = tornado.web.Application(
    [
        ('/', IndexHandler),
        ('/endpoint', EndpointHandler),
    ],
    template_path=os.path.join('/', 'opt', 'project', 'project', 'templates'),
    static_path=os.path.join('/', 'opt', 'project', 'project', 'static')
)

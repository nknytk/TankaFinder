# coding: utf-8

import os
import sys
from urllib.parse import parse_qsl

from wheezy.web.handlers import BaseHandler, file_handler
from wheezy.routing import url
from wheezy.http import WSGIApplication
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory

APP_HOME = os.path.dirname(__file__)
sys.path.append(APP_HOME)
import uta


class APIHandler(BaseHandler):
    def post(self):
        req_param = self.request.environ['wsgi.input'].read(int(self.request.environ.get('CONTENT_LENGTH', 0)))
        qdic = dict(parse_qsl(req_param.decode('UTF-8')))
        return self.handle(qdic)

    def get(self):
        qdic = dict(parse_qsl(self.request.environ.get('QUERY_STRING', '')))
        return self.handle(qdic)

    def handle(self, qdic):
        syllable_pattern = uta.HAIKU if qdic.get('syllable_pattern') == 'HAIKU' else uta.TANKA
        txt = qdic.get('txt', '')
        found_uta = uta.main(txt, syllable_pattern)

        return self.json_response(found_uta)


routing_rules = [
    url('static/{path:any}', file_handler(root='static'), name='static'),
    url('api', APIHandler, name='api')
]

main = WSGIApplication([
    bootstrap_defaults(url_mapping=routing_rules),
    path_routing_middleware_factory
], {})


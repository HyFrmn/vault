"""The base Controller API

Provides the BaseController class for subclassing.
"""
import re
import datetime
import simplejson

from pylons import request
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

import vault.model as model
from vault.model import meta, Resource, Project

map_pattern = re.compile(r'^(?P<dict>[A-Za-z-_]+)\[(?P<key>[A-Za-z-_]+)\]$')

__all__ = ['meta',
           'model',
           'render',
           'to_json',
           'BaseController',
           'Resource',
           'Project',]

class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Resource):
            return obj.to_dict()
        if isinstance(obj, datetime.datetime):
            return str(obj)
        if hasattr(obj, '__iter__'):
            serialized = list()
            for o in obj:
                serialized.append(self.default(o))
            return serialized
        return simplejson.JSONEncoder.default(self, obj)

def to_json(obj):
    return simplejson.dumps(obj, cls=JSONEncoder)

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

    def __before__(self):
        self.params = self.parse_params(request.params)

    def parse_params(self, params):
        output = {}
        for k, v in params.iteritems():
            match = map_pattern.match(k)
            if match:
                key = match.group('key')
                d = match.group('dict')
                if not output.has_key(d):
                    output[d] = dict()
                output[d][key] = v
            else:
                output[k] = v
        return output

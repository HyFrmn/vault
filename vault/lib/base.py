"""The base Controller API

Provides the BaseController class for subclassing.
"""
import re
import datetime
import simplejson

from pylons import request
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import vault.model as model
from vault.model import *

map_pattern = re.compile(r'^(?P<dict>[A-Za-z-_]+)\[(?P<key>[A-Za-z-_]+)\]$')

__all__ = ['meta',
           'model',
           'render',
           'to_json',
           'BaseController',
           'Resource',
           'Project',
           'Preview',
           'Asset',
           'Task',
           'Version',
           'User',
           'Comment']

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
    return simplejson.dumps(obj, cls=JSONEncoder, indent=4)

class BaseController(WSGIController):
    requires_auth = False
    
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
        if self.requires_auth and 'user' not in session:
            #Redirect to login
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(controller='login', action='login')
        else:
            self.current_user = meta.Session.query(User).filter(User.username==session['user']).first()

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

"""The base Controller API

Provides the BaseController class for subclassing.
"""
import datetime
import simplejson

from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from vault.model import meta, Resource

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

    def to_json(self, obj):
        return simplejson.dumps(obj, cls=JSONEncoder)
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

class ApplicationController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/application.mako')
        # or, return a response
        return render('/application.mako')

    def menu(self):
        node = self.params.get('node', None)
        if node:
            if ':' in node:
                type_, id = node.split(':')
                data = meta.Session.query(Resource).filter(Resource.id==id).first().children
            else:
                data = meta.Session.query(Project).all()
        else:
            data = meta.Session.query(Project).all()
        return to_json(map(lambda x: {'text' : x.title, 'id' : '%s:%s' % (x._classname, x.id) }, data))
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

def _build_menu_item(item):
    if item:
        data = {'text' : item.title, 
            'id' : '%s:%s' % (item._classname, item.id)}
        if not item.children:
            data['leaf'] = True
        return data


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
        return to_json(map(_build_menu_item, data))
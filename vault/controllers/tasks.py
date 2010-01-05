import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class TasksController(ResourcesController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')
    _poly_class_ = Task

    def index(self, format='html'):
        """GET /projects: All items in the collection"""
        resource_id = self.params.get('resource_id', None)
        parent_id = self.params.get('parent_id', None)
        if resource_id:
            c.resources = meta.Session.query(Resource).filter(Resource.id==resource_id).all()
        elif parent_id:
            q = meta.Session.query(Task).filter(Task.asset_id==parent_id).all()
            if q:
                c.resources = q
            else:
                c.resources = []
        else:
            c.resources = meta.Session.query(self._poly_class_).all()
        if format in ['js','json']:
            #Render JSON
            response.headers['Content-Type'] = 'application/javascript'
            return to_json({self._classname() : c.resources})
        if format == 'xmlrpc':
            return to_dict({self._classname() : c.resources})
        return render("/%s/index.mako" % self._classname())
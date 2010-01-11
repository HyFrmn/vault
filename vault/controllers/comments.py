import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class CommentsController(ResourcesController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')
    _poly_class_ = Comment
    requires_auth = True

    def new(self, format='html'):
        """GET /projects/new: Form to create a new item"""
        defaults = {}
        resource_id = self.params.get('resource_id', None)
        if resource_id:
            defaults['resource'] = meta.Session.query(Resource).filter(Resource.id==resource_id).first()
        if format in ['json', 'js']:
            return to_json(self._poly_class_.form_schema(self._poly_class_.new_form_fields(), defaults))

    def create(self, commit=True):
        """POST /projects: Create a new item"""
        # url('projects')
        self._before_create()
        log.info('Creating Resource (%s), %s' % (self._poly_class_.__tablename__, self.params[self._classname()]))
        c.resource = self._poly_class_(**self.params[self._classname()])
        c.resource.user = self.current_user
        meta.Session.add(c.resource)
        if commit:
            meta.Session.commit()
        return to_json({ 'data' : c.resource, "success" : True, 'view' : { 'xtype' : 'vault.details', 'rid' : c.resource.id, 'rtype' : c.resource.__tablename__ }})
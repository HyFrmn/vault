import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class AssetsController(ResourcesController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')
    _poly_class_ = Asset

    def new(self, format='html'):
        """GET /projects/new: Form to create a new item"""
        defaults = {}
        parent_id = self.params.get('parent_id', None)
        if parent_id:
            defaults['parent_id'] = int(parent_id)
        project_id = self.params.get('project_id', None)
        if project_id:
            defaults['project_id'] = int(project_id)
        if format in ['json', 'js']:
            return to_json(self._poly_class_.form_schema(self._poly_class_.new_form_fields(), defaults))

    def create(self, commit=True):
        """POST /assets: Create a new item"""
        # url('projects')
        self._before_create()
        project_id = self.params[self._classname()].get('project_id', None)
        if not project_id:
            return to_json({ "success" : False })
        else:
            project = Project.find(project_id)
            if not project:
                return to_json({ "success" : False })
        log.info('Creating Asset (%s), %s' % (self._poly_class_.__tablename__, self.params[self._classname()]))
        c.resource = project.create_asset(**self.params[self._classname()])
        meta.Session.add(c.resource)
        parent_id = self.params[self._classname()].get('parent_id', None)
        if parent_id:
            parent = meta.Session.query(Resource).filter(Resource.id==int(parent_id)).first()
            parent.children.append(c.resource)
        for k, v in c.resource.__dict__.copy().iteritems():
            if k.endswith('_id'):
                id_attr = getattr(c.resource, k)
                relation_attr = k[:-3]
                relation = getattr(c.resource, relation_attr)
                if id_attr and not relation:
                        relation = meta.Session.query(Resource).filter(Resource.id==int(id_attr)).first()
                        setattr(c.resource, relation_attr, relation)
        if commit:
            meta.Session.commit()
        return to_json({ 'data' : c.resource, "success" : True, 'view' : { 'xtype' : 'vault.details', 'rid' : c.resource.id, 'rtype' : c.resource.__tablename__ }})

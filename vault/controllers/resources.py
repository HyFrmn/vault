import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

class ResourcesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('resource', 'resources')
    _poly_class_ = Resource

    def _classname(self):
        return self._poly_class_.__tablename__

    def index(self, format='html'):
        """GET /projects: All items in the collection"""
        resource_id = self.params.get('resource_id', None)
        parent_id = self.params.get('parent_id', None)
        project_id = self.params.get('project_id', None)
        if resource_id:
            c.resources = meta.Session.query(Resource).filter(Resource.id==resource_id).all()
        elif project_id:
            q = meta.Session.query(Project).filter(Project.id==project_id).first()
            if q:
                c.resources = q.children
            else:
                c.resources = []
        elif parent_id:
            q = meta.Session.query(Resource).filter(Resource.id==parent_id).first().children
            if q:
                c.resources = q.children
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

    def _before_create(self):pass

    def create(self, commit=True):
        """POST /projects: Create a new item"""
        # url('projects')
        self._before_create()
        log.info('Creating Resource (%s), %s' % (self._poly_class_.__class__.__name__, self.params[self._classname()]))
        c.resource = self._poly_class_(**self.params[self._classname()])
        meta.Session.add(c.resource)
        parent_id = self.params[self._classname()].get('parent_id', None)
        if parent_id:
            parent = meta.Session.query(Resource).filter(Resource.id==int(parent_id)).first()
            parent.children.append(c.resource)
        for k, v in c.resource.__dict__.copy().iteritems():
            print k, v
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

    def new(self, format='html'):
        """GET /projects/new: Form to create a new item"""
        defaults = {}
        parent_id = self.params.get('parent_id', None)
        if parent_id:
            defaults['parent_id'] = int(parent_id)
        if format in ['json', 'js']:
            return to_json(self._poly_class_.form_schema(self._poly_class_.new_form_fields(), defaults))

    def update(self, id):
        """PUT /projects/id: Update an existing item"""
        c.resource = meta.Session.query(self._poly_class_).filter(Resource.id==id).first()
        c.resource.update(self.params[self._classname()])
        meta.Session.commit()
        return to_json({ 'data' : c.resource, "success" : True, 'view' : { 'xtype' : 'vault.details', 'rid' : c.resource.id }})

    def delete(self, id):
        """DELETE /projects/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('project', id=ID),
        #           method='delete')
        # url('project', id=ID)

    def show(self, id, format='html'):
        """GET /projects/id: Show a specific item"""
        c.resource = meta.Session.query(self._poly_class_).filter(Resource.id==id).first()
        if format in ['js','json']:
            #Render JSON
            response.headers['Content-Type'] = 'application/javascript'
            return to_json({'data' : c.resource, 'tmpl' : render('/%s/details.xtpl' % self._classname())})
        return render("/%s/details.mako" % self._classname())

    def edit(self, id, format='html'):
        """GET /projects/id/edit: Form to edit an existing item"""
        c.resource = meta.Session.query(self._poly_class_).filter(Resource.id==id).first()
        if format in ['json', 'js']:
            return to_json(self._poly_class_.form_schema(c.resource.edit_form_fields()))

    def dump(self):
        return str(self.parse_params(request.params))
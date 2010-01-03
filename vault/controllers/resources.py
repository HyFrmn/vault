import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

tmpl = """<div class="details">
    <tpl for=".">
        <img src="{image}"><div class="details-info">
        {image}
        <p>
            <b>Title:</b>
            <span>{title}</span>
        </p>
        <p>
            <b>Last Modified:</b>
            <span>{modified}</span></div>
            <p>{description}</p>
        </p>
    </tpl>
</div>
"""

class ResourcesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('resource', 'resources')
    _poly_class_ = Resource

    def _classname(self):
        return self._poly_class_.__name__.lower()

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
                c.resource = []
        elif parent_id:
            q = meta.Session.query(Resource).filter(Resource.id==parent_id).first().children
            if q:
                c.resources = q.children
            else:
                c.resource = []
        else:
            c.resources = meta.Session.query(self._poly_class_).all()
        if format in ['js','json']:
            #Render JSON
            response.headers['Content-Type'] = 'application/javascript'
            return to_json({self._classname() : c.resources})
        return render("/%s/index.mako" % self._classname())

    def _before_create(self):pass

    def create(self, commit=True):
        """POST /projects: Create a new item"""
        # url('projects')
        self._before_create()
        log.info('Creating Resource, %s' % self.params[self._classname()])
        c.resource = self._poly_class_(**self.params[self._classname()])
        meta.Session.add(c.resource)
        parent_id = self.params[self._classname()].get('parent_id', None)
        if parent_id:
            parent = meta.Session.query(Resource).filter(Resource.id==int(parent_id)).first()
            parent.children.append(c.resource)
        if commit:
            meta.Session.commit()
        return to_json({ 'data' : c.resource, "success" : True, 'view' : { 'xtype' : 'vault.details', 'rid' : c.resource.id }})

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
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('project', id=ID),
        #           method='put')
        # url('project', id=ID)

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
        c.resources = meta.Session.query(self._poly_class_).filter(Resource.id==id).first()
        if format in ['js','json']:
            #Render JSON
            response.headers['Content-Type'] = 'application/javascript'
            return to_json({'data' : c.resources, 'tmpl' : tmpl})
        return render("/%s/index.mako" % self._classname())

    def edit(self, id, format='html'):
        """GET /projects/id/edit: Form to edit an existing item"""
        # url('edit_project', id=ID)

    def dump(self):
        return str(self.parse_params(request.params))
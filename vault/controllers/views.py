import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

project_dashboard_view = {
                          'title' : "Project",
                          'layout' : "border",
                          'items': [{
                                     'xtype' : 'vault.details',
                                     'region' : 'center'
                                     },{
                                      'xtype' : 'vault.grid',
                                      'region' : 'south',
                                      'height' : '250',
                                      'split' : True,
                                      'resultPanel' : 'Vault.mainPanel'
                                     }],
                          }

class ViewsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('view', 'views')

    def index(self, format='html'):
        """GET /projects: All items in the collection"""
        if format in ['js','json']:
            #Render JSON
            response.headers['Content-Type'] = 'application/javascript'
            return to_json(project_dashboard_view)
        return render("/%s/index.mako" % self._classname())
        # url('views')

    def create(self):
        """POST /views: Create a new item"""
        # url('views')

    def new(self, format='html'):
        """GET /views/new: Form to create a new item"""
        # url('new_view')

    def update(self, id):
        """PUT /views/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('view', id=ID),
        #           method='put')
        # url('view', id=ID)

    def delete(self, id):
        """DELETE /views/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('view', id=ID),
        #           method='delete')
        # url('view', id=ID)

    def show(self, id, format='html'):
        """GET /views/id: Show a specific item"""
        # url('view', id=ID)

    def edit(self, id, format='html'):
        """GET /views/id/edit: Form to edit an existing item"""
        # url('edit_view', id=ID)

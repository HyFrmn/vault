import logging

from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

def _build_menu_item(item):
    if item:
        data = {'text' : item.title, 
                'id' : '%s:%s' % (item.id, item._classname)}
        data['icon'] = item.icon
        data['project_id'] = item.id
        if not isinstance(item, Project):
            if not item.children:
                data['leaf'] = True
                data['view'] = { 'xtype' : 'vault.details', 'storeId' : item.id, 'rid' : item.id, 'rtype' : item._classname }
        else:
            data['view'] = { 'xtype' : 'vault.projectdashboard', 'project_id' : item.id, 'title': item.title }
            data['children'] = [{ 'text' : 'Assets',
                                  'id' : '%d:project-assets' % item.id,
                                  'view': { 'xtype' : 'vault.assetgrid' },
                                  'leaf' : True,
                                  'project_id' : item.id,
                                },{ 'text' : 'Tasks',
                                  'id' : '%d:project-tasks' % item.id,
                                  'view': { 'xtype' : 'vault.taskgrid' },
                                  'leaf' : True,
                                  'project_id' : item.id,
                                },{ 'text' : 'Versions',
                                  'id' : '%d:project-versions' % item.id,
                                  'view': { 'xtype' : 'vault.versiongrid' },
                                  'leaf' : True,
                                  'project_id' : item.id,
                                }]
        return data


class ApplicationController(BaseController):
    requires_auth = True

    def index(self):
        return render('/application.mako')

    def user(self):
        return self.current_user.username

    def toolbar(self):
        return to_json(['->', self.current_user.username])

    def menu(self):
        node = self.params.get('node', None)
        if node:
            if ':' in node:
                id, type_ = node.split(':')
                data = meta.Session.query(Resource).filter(Resource.id==id).all()
            else:
                data = meta.Session.query(Project).all()
        else:
            data = meta.Session.query(Project).all()
        return to_json(map(_build_menu_item, data))

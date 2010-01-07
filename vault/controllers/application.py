import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

def dashboard(project):
    data = [{
    'layout' : 'border',
    'items' : [{
                   'region':'center',
                   'id' : 'dashboard-grid',
                   'rtype' : 'assets',
                   'xtype' : 'vault.resourcedataview',
                   'tbarItems' :  [{'xtype' : 'vault.open_form_dialog_button',
                           'text' : 'New Asset',
                           'dialogConfig' : project.new_dialog_config(rtype='assets', title='New Asset (%s)' % project.title, parent_id=project.id), 
                           'storeParams': { 'parent_id' : project.id }
                        },{'xtype' : 'vault.open_form_dialog_button',
                           'text' : 'New Preview',
                           'dialogConfig' : project.new_dialog_config(rtype='previews', title='New Preview (%s)' % project.title, parent_id=project.id) ,
                        },{
                          'text' : 'Edit',
                          'xtype' : 'vault.open_form_dialog_button',
                          'dialogConfig' : project.edit_dialog_config(),
                          'parentPanel' : "dashboard-grid",
                          'rtype' : 'resources',
                        }]
               },{
                  'xtype' : 'tabpanel',
                  'region' : 'south',
                  'height' : 325,
                  'activeTab' : 0,
                  'split' : True,
                  'border' : False,
                  'items' : [{
                              'title' : 'Details',
                              'id' : 'dashboard-details',
                              'xtype': 'vault.layoutpanel',
                              'autoScroll' : True,
                              'split' : True,
                              'height': 325,
                              'items':[{
                                        'xtype' : 'vault.details',
                                        'rid' : 1,
                                        'title' : None,
                                        'autoScroll' : True,
                                        'listenTo' : 'Ext.getCmp("dashboard-grid")',
                                        }]
                              },{
                                 'title' : 'Versions',
                                 'id' : 'dashboard-versions',
                                 'xtype': 'vault.layoutpanel',
                                 'autoScroll' : True,
                                 'split' : True,
                                 'height': 325,
                                 'items':[{
                                           'xtype' : 'vault.grid',
                                           'rid' : 1,
                                           'title' : None,
                                           'autoScroll' : True,
                                           'rtype': 'versions',
                                           'listenTo': 'Ext.getCmp("dashboard-grid")',
                                           }]
                                 },{
                                    'title' : 'Previews',
                                    'id' : 'dashboard-previews',
                                    'xtype': 'vault.layoutpanel',
                                    'autoScroll' : True,
                                    'split' : True,
                                    'height': 325,
                                    'items':[{
                                              'xtype' : 'vault.grid',
                                              'rid' : 1,
                                              'title' : None,
                                              'autoScroll' : True,
                                              'rtype': 'previews',
                                              }]
                                    },{
                                       'title' : 'Tasks',
                                       'id' : 'dashboard-tasks',
                                       'xtype': 'vault.layoutpanel',
                                       'autoScroll' : True,
                                       'split' : True,
                                       'height': 325,
                                       'items':[{
                                                 'xtype' : 'vault.grid',
                                                 'rid' : 1,
                                                 'title' : None,
                                                 'autoScroll' : True,
                                                 'rtype': 'tasks',
                                                 'listenTo': 'Ext.getCmp("dashboard-grid")',
                                                 }]
                                       }]
                            }]
                  }]
    return data

def _build_menu_item(item):
    if item:
        data = {'text' : item.title, 
            'id' : '%s:%s' % (item.id, item._classname)}
        data['icon'] = item.icon
        if not isinstance(item, Project):
            if not item.children:
                data['leaf'] = True
                data['view'] = { 'xtype' : 'vault.details', 'storeId' : item.id, 'rid' : item.id, 'rtype' : item._classname }
        else:
            data['view'] = dashboard(item)
            data['children'] = [{ 'text' : 'Assets',
                                  'id' : '%d:project-assets' % item.id,
                                  'view': item.grid_config(),
                                  'leaf' : True 
                                },{ 'text' : 'Tasks',
                                  'id' : '%d:project-tasks' % item.id,
                                  'view': item.grid_config(),
                                  'leaf' : True 
                                },{ 'text' : 'Versions',
                                  'id' : '%d:project-versions' % item.id,
                                  'view': item.grid_config(),
                                  'leaf' : True 
                                }]
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
                id, type_ = node.split(':')
                data = meta.Session.query(Resource).filter(Resource.id==id).all()
            else:
                data = meta.Session.query(Project).all()
        else:
            data = meta.Session.query(Project).all()
        return to_json(map(_build_menu_item, data))

import os
import imp

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource
from previewable import Previewable
from asset import Asset

class Project(Previewable):
    __tablename__ = 'projects'

    icon = '/icons/folder.png'

    # Relational
    id = Column(Integer, ForeignKey('previewables.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'project'}
    assets = relation(Asset, primaryjoin=id==Asset.project_id, backref="project")

    # Data
    client = Column(String(255), default='')

    root_dir = Column(String(255), default='')
    asset_dir = Column(String(255), default='')
    config_dir = Column(String(255), default='')

    def _update_client(self, client):
        self.client = str(client)

    def _update_root_dir(self, client):
        self.client = str(client)

    def _update_asset_dir(self, client):
        self.client = str(client)

    def _update_config_dir(self, client):
        self.client = str(client)

    def grid_config(self,  **kwargs):
        data = Resource.grid_config(self)
        data['title'] = self.title
        data['tbar'] = [{
                         'text' : 'New',
                         'layout' : 'fit',
                         'menu' : {
                                   'items' : [{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Asset',
                                              'dialogConfig' : self.new_dialog_config(rtype='assets', title='New Asset (%s)' % self.title, parent_id=self.id), 
                                              'storeParams': { 'parent_id' : self.id }
                                           },{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Task',
                                              'dialogConfig' : self.new_dialog_config(rtype='tasks', title='New Task (%s)' % self.title, parent_id=self.id) ,
                                           },{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Preview',
                                              'dialogConfig' : self.new_dialog_config(rtype='previews', title='New Preview (%s)' % self.title, parent_id=self.id) ,
                                           }]
                                   }
                         },{
                         'text' : 'Edit',
                         'xtype' : 'vault.open_form_dialog_button',
                         'dialogConfig' : self.edit_dialog_config(kwargs),
                         'parentPanel' : 'project-grid',
                         'rtype' : 'resources',
                         }]
        data['storeParams'] = { 'project_id' : self.id }
        data.update(kwargs)
        return data

    def to_dict(self):
        data = Resource.to_dict(self)
        data['client'] = str(self.client)
        return data

    def _update_client(self, client):
        self.client = str(client)

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields['client'] = {'fieldLabel' : 'Client'}
        fields['preview'] = { 'fieldLabel' : 'Preview' , 'xtype' : 'vault.resourcelinkfield', 'rtype' : 'previews'}
        return fields

    def create_asset(self, **kwargs):
        asset = Asset(**kwargs)
        asset.project = self
        if self.config_dir:
            project_module_path = os.path.join(self.config_dir, 'project.py')  
            if os.path.exists(project_module_path):
                module = imp.load_source('action_module', project_module_path)
                func = getattr(module, 'create_asset_callback')
                func(asset)
                del module
        return asset
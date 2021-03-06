import os
import imp

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource
from previewable import Previewable
from asset import Asset
from task import Task
from task_template import TaskTemplate

class Project(Previewable):
    __tablename__ = 'projects'

    icon = '/icons/folder.png'

    # Relational
    id = Column(Integer, ForeignKey('previewables.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'projects'}
    assets = relation(Asset, primaryjoin=id==Asset.project_id, backref="project")

    # Data
    client = Column(String(255), default='')

    root_dir = Column(String(255), default='')
    asset_dir = Column(String(255), default='')
    config_dir = Column(String(255), default='')
    module_dir = Column(String(255), default='')

    def _parse_dir_arg(self, arg):
        arg = str(arg)
        if os.path.isabs(arg):
            return arg
        else:
            if self.root_dir:
                return os.path.join(self.root_dir, arg)
            else:
                return None

    def to_dict(self):
        data = Resource.to_dict(self)
        data['client'] = str(self.client)
        return data

    def _update_client(self, arg):
        self.client = self._parse_dir_arg(arg)

    def _update_root_dir(self, arg):
        self.root_dir = self._parse_dir_arg(arg)

    def _update_asset_dir(self, arg):
        self.asset_dir = self._parse_dir_arg(arg)

    def _update_config_dir(self, arg):
        self.config_dir = self._parse_dir_arg(arg)

    def _update_module_dir(self, arg):
        self.module_dir = self._parse_dir_arg(arg)

    def _update_client(self, client):
        self.client = str(client)

    def create_asset(self, **kwargs):
        asset = Asset(**kwargs)
        asset.project = self
        if asset.template.meta.get('tasks', None):
            for task_tmpl_name in asset.template.meta['tasks']:
                tmpl = TaskTemplate.find_by_name(task_tmpl_name)
                if tmpl:
                    task = asset.TaskFromTemplate(tmpl)
                    asset.tasks.append(task)
        if self.module_dir:
            project_module_path = os.path.join(self.module_dir, 'project.py') 
            if os.path.exists(project_module_path):
                module = imp.load_source('action_module', project_module_path)
                if hasattr(module, 'create_asset_callback'):
                    func = getattr(module, 'create_asset_callback')
                    func(asset)
                if asset.template:
                    attr = 'create_asset_callback_' + asset.template.name
                    if hasattr(module, attr):
                        func = getattr(module, attr)
                        func(asset)
                del module
            else:
                print 'WARNING: Could not find module [%s]' % project_module_path
        return asset

    #Form Helpers 
    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields['client'] = {'fieldLabel' : 'Client'}
        fields['preview'] = { 'fieldLabel' : 'Preview' , 'xtype' : 'vault.resourcelinkfield', 'rtype' : 'previews'}
        return fields
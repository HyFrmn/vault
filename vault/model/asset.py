from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list

from meta import Session

from resource import Resource, Session, DictionaryDecorator

from previewable import Previewable
from asset_template import AssetTemplate
from task import Task

class Asset(Previewable):
    __tablename__ = 'assets'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('previewables.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset'}
    template_id = Column(Integer, ForeignKey('asset_templates.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    meta = Column(DictionaryDecorator(16384), default={})
    tasks = relation(Task, primaryjoin=Task.asset_id==id,
                     collection_class=ordering_list('order'),
                    backref='asset')
    def _update_meta(self, meta):
        if self.meta:
            self.meta.update(meta)
        else:
            self.meta = meta
    
    def _update_template_name(self, name):
        template = Session.query(AssetTemplate).filter(AssetTemplate.name==name).first()
        self.template = template

    def to_dict(self):
        data = Previewable.to_dict(self)
        if self.project:
            data['project_id'] = int(self.project.id)
            data['project_name'] = str(self.project.name)
            data['project_title'] = str(self.project.title)
        else:
            data['project_id'] = None
            data['project_name'] = None
            data['project_title'] = None
        return data

    def grid_config(self):
        data = Resource.grid_config(self)
        data['title'] = self.title
        data['tbar'] = [{
                         'text' : 'New',
                         'menu' : {
                                   'items' : [{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Asset',
                                              'dialogConfig' : self.new_dialog_config(self.id, type_='resources')
                                           },{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Preview',
                                              'dialogConfig' : self.new_dialog_config(self.id, type_='previews')
                                           }]
                                   }
                         }]
        data['storeParams'] = { 'parent_id' : self.id }
        return data

    @classmethod
    def new_form_fields(cls):
        fields = Previewable.new_form_fields()
        fields['template_name'] = { 'fieldLabel' : 'Template Name' , 'value' : 'realtime_model' }
        fields['project_id'] = { 'fieldLabel' : 'Project' , 'xtype' : 'hidden' }
        return fields

    def TaskFromTemplate(self, tmpl):
        task = Task.FromTemplate(tmpl)
        task.title = self.title + ' ' + task.title
        task.name = self.name + '_' + task.name
        self.tasks.append(task)
        return task

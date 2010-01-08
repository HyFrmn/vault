from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource, Session

from previewable import Previewable

class Asset(Previewable):
    __tablename__ = 'assets'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('previewable.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset'}

    #template_id = Column(Integer, ForeignKey('asset_templates.id'))
    #template = relation("AssetTemplate", primaryjoin="Asset.template_id==AssetTemplate.id")

    #project_id = Column(Integer, ForeignKey('projects.id'))
    #project = relation("Project", primaryjoin="Asset.project_id==Project.id", foreign_keys=['Asset.project_id', 'Project.id'])

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
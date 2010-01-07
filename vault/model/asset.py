from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource, Session
from preview import Preview
from previewable import Previewable

class Asset(Previewable):
    __tablename__ = 'assets'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('previewables.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset'}

    def to_dict(self):
        data = Resource.to_dict(self)
        if self.preview:
            for k, v in self.preview.to_dict().iteritems():
                data['preview_' + k] = v
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

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Time, Float
from sqlalchemy.orm import relation

from resource import Resource, odict
from asset import Asset

class Task(Resource):
    __tablename__ = 'tasks'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'task'}

    # Data
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relation(Asset, primaryjoin=asset_id==Asset.__table__.c.id)
    meta = Column(Text)
    estimate = Column(Float)
    parent_id = Column(Integer, ForeignKey('tasks.id'))
    parent = relation("Task", primaryjoin=parent_id==id)

    def to_dict(self):
        data = Resource.to_dict(self)
        print 'Creating Dictionary for JSON output.'
        if self.asset:
            for k, v in self.asset.to_dict().iteritems():
                data['asset_' + k] = v
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
        #fields = Resource.new_form_fields()
        fields = odict()
        fields['asset'] = { 'fieldLabel' : 'Asset' , 'xtype' : 'vault.resourcelinkfield', 'rtype' : 'assets' }
        fields['estimate'] = { 'fieldLabel' : 'Estimated Time' , 'xtype' : 'numberfield' }
        return fields

#Black Magic
Resource._register(Task)
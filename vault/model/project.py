from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Project(Resource):
    __tablename__ = 'projects'

    icon = '/icons/folder.png'

    # Relational
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'project'}

    # Data
    client = Column(String(255))
    preview = Column(Integer, ForeignKey('previews.resource_id'))

    root_dir = Column(String(255))
    asset_dir = Column(String(255))
    config_dir = Column(String(255))
    
    def to_dict(self):
        data = Resource.to_dict(self)
        data['client'] = str(self.client)
        return data

    def grid_config(self):
        data = Resource.grid_config(self)
        data['title'] = self.title
        data['tbar'] = [{
                         'text' : 'New',
                         'menu' : {
                                   'items' : [{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Asset',
                                              'dialogConfig' : self.new_dialog_config(self.id, type_='assets', title='New Asset (%s)' % self.title)
                                           },{'xtype' : 'vault.open_form_dialog_button',
                                              'text' : 'New Preview',
                                              'dialogConfig' : self.new_dialog_config(self.id, type_='previews', title='New Preview (%s)' % self.title)
                                           }]
                                   }
                         }]
        data['storeParams'] = { 'project_id' : self.id }
        return data

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields.insert(2, ('client', 'Client'))
        return fields
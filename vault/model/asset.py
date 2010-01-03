from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Asset(Resource):
    __tablename__ = 'assets'

    icon = '/icons/pill.png'

    # Relational
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset'}

    # Data
    preview = Column(Integer, ForeignKey('previews.resource_id'))

    def to_dict(self):
        data = Resource.to_dict(self)
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
        fields = Resource.new_form_fields()
        return fields
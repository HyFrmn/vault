from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource
from preview import Preview

class Project(Resource):
    __tablename__ = 'projects'

    icon = '/icons/folder.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'project'}

    # Data
    client = Column(String(255))
    #preview_id = Column(Integer, ForeignKey('previews.id'))
    #preview = relation(Preview)

    root_dir = Column(String(255))
    asset_dir = Column(String(255))
    config_dir = Column(String(255))
    
    def to_dict(self):
        data = Resource.to_dict(self)
        data['client'] = str(self.client)
        return data

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
                         }]
        data['storeParams'] = { 'project_id' : self.id }
        data.update(kwargs)
        return data

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields['client'] = {'fieldLabel' : 'Client'}
        fields['preview'] = { 'fieldLabel' : 'Preview' , 'xtype' : 'vault.resourcelinkfield' }
        return fields
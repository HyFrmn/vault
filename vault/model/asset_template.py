from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource, Session
from preview import Preview

class AssetTemplate(Resource):
    __tablename__ = 'asset_templates'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset_template'}

    def to_dict(self):
        data = Resource.to_dict(self)
        return data

    def grid_config(self):
        data = Resource.grid_config(self)
        data['title'] = self.title
        data['tbar'] = [{
                       'items' : [{'xtype' : 'vault.open_form_dialog_button',
                                  'text' : 'New Asset',
                                  'iconSrc' : 'icons/add.png',
                                  'dialogConfig' : self.new_dialog_config(self.id, type_='resources')
                               }]
                         }]
        data['storeParams'] = { 'parent_id' : self.id }
        return data

    def _update_preview_id(self, preview_id):
        try:
            id = int(preview_id)
        except ValueError:
            id = 0
        if id:
            preview = Session.query(Resource).filter(Resource.id==id).first()
            self.preview = preview

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields['preview'] = { 'fieldLabel' : 'Preview' , 'xtype' : 'vault.resourcelinkfield', 'rtype' : 'previews' }
        return fields
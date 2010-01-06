from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource, Session
from preview import Preview

class Asset(Resource):
    __tablename__ = 'assets'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset'}

    # Data
    preview_id = Column(Integer, ForeignKey('previews.id'))
    preview = relation(Preview, primaryjoin=preview_id==Preview.__table__.c.id)

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
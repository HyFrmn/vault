from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource, Session
from preview import Preview

class Previewable(Resource):
    __tablename__ = 'previewables'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'previewables'}

    # Data
    preview_id = Column(Integer, ForeignKey('previews.id'))
    preview = relation(Preview, primaryjoin=preview_id==Preview.__table__.c.id)

    def to_dict(self):
        data = Resource.to_dict(self)
        if self.preview:
            data['preview_id'] = int(self.preview.id)
            data['preview_name'] = str(self.preview.name)
            data['preview_title'] = str(self.preview.title)
            data['preview_image'] = str(self.preview.image)
        else:
            data['preview_id'] = None
            data['preview_name'] = None
            data['preview_image'] = None
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
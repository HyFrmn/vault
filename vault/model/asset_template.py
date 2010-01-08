from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from resource import Resource, Session, DictionaryDecorator
from preview import Preview

class AssetTemplate(Resource):
    __tablename__ = 'asset_templates'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset_template'}

    meta = Column(DictionaryDecorator(16384), default={})
    type = Column(String(64), default='')

    def _update_type(self, type):
        self.type = str(type.replace('.', '_'))

    def _update_meta(self, meta):
        if self.meta:
            self.meta.update(meta)
        else:
            self.meta = {}

    type = Column(String(64))
    meta = Column(Text)

    def to_dict(self):
        data = Resource.to_dict(self)
        return data
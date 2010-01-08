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

    meta = Column(Text)

    def to_dict(self):
        data = Resource.to_dict(self)
        return data
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.ext.orderinglist import ordering_list

from meta import Base, Session
from resource import Resource, Session, DictionaryDecorator
from preview import Preview
from task_template import TaskTemplate

class TemplateConnection(Base):
    __tablename__ = 'template_connections'

    # Relational
    asset_template_id = Column(Integer, ForeignKey('asset_templates.id'), primary_key=True)
    task_template_id = Column(Integer, ForeignKey('task_templates.id'), primary_key=True)

    def __init__(self, parent_id, child_id):
        self.asset_template_id = parent_id
        self.task_template_id = child_id

class AssetTemplate(Resource):
    __tablename__ = 'asset_templates'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset_templates'}

    meta = Column(DictionaryDecorator(16384), default={})

    def _update_meta(self, meta):
        if self.meta:
            self.meta.update(meta)
        else:
            self.meta = meta

    def to_dict(self):
        data = Resource.to_dict(self)
        return data
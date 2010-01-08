from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation

from meta import Session
from resource import Resource, Session, DictionaryDecorator
from preview import Preview

class TaskTemplate(Resource):
    __tablename__ = 'task_templates'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'task_template'}

    meta = Column(DictionaryDecorator(16384), default={})

    def _update_meta(self, meta):
        if self.meta:
            self.meta.update(meta)
        else:
            self.meta = meta

    def to_dict(self):
        data = Resource.to_dict(self)
        data['meta'] = self.meta
        return data

    @classmethod
    def find_by_name(cls, name):
        return Session.query(cls).filter(cls.name==name).first()
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Time, Float
from sqlalchemy.orm import relation

from resource import Resource, odict, Session

class Comment(Resource):
    __tablename__ = 'comments'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'comment'}

    # Data
    resource_id = Column(Integer, nullable=False)
    meta = Column(Text)
    parent = relation(Resource, primaryjoin=resource_id==Resource.id, foreign_keys=[resource_id])

    @classmethod
    def FromTemplate(cls, tmpl):
        task = cls.__call__(name=tmpl.name, title=tmpl.title)
        return task

    def to_dict(self):
        data = Resource.to_dict(self)
        if self.asset:
            for k, v in self.asset.to_dict().iteritems():
                data['asset_' + k] = v
        return data

    @classmethod
    def new_form_fields(cls):
        #fields = Resource.new_form_fields()
        fields = Resource.new_form_fields()
        return fields

    def _edit_form_fields(self):
        return self.new_form_fields()

    def _update_resource_id(self, asset_id):
        try:
            id = int(asset_id)
        except ValueError:
            id = 0
        if id:
            asset = Session.query(Resource).filter(Resource.id==id).first()
            self.asset = asset

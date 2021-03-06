from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Time, Float
from sqlalchemy.orm import relation

from resource import Resource, odict, Session

class Task(Resource):
    __tablename__ = 'tasks'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'tasks'}

    # Data
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    meta = Column(Text)
    estimate = Column(Float)
    order = Column(Integer)
    status = Column(Integer, default=0)
    template_id = Column(Integer, ForeignKey('task_templates.id'))

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
        fields['asset'] = { 'fieldLabel' : 'Asset' , 'xtype' : 'vault.resourcelinkfield', 'rtype' : 'assets' }
        fields['estimate'] = { 'fieldLabel' : 'Estimated Time' , 'xtype' : 'numberfield' }
        return fields

    def _edit_form_fields(self):
        return self.new_form_fields()

    def _update_asset_id(self, asset_id):
        try:
            id = int(asset_id)
        except ValueError:
            id = 0
        if id:
            asset = Session.query(Resource).filter(Resource.id==id).first()
            self.asset = asset

#Black Magic
Resource._register(Task)
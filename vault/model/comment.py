from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Time, Float
from sqlalchemy.orm import relation

from resource import Resource, odict, Session
from user import User

class Comment(Resource):
    __tablename__ = 'comments'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'comments', 'inherit_condition' : id==Resource.id}

    # Data
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relation(User)
    resource_id = Column(Integer, ForeignKey('resources.id'))

    def _init_setup(self):
        if self.resource:
            self.title = 'Comment on "%s"' % self.resource.title
            self.name = "%s_comment" % self.resource.name

    def to_dict(self):
        data = Resource.to_dict(self)
        if self.resource:
            data['resource_title'] = self.resource.title
            data['resource_name'] = self.resource.name
            data['resource_id'] = self.resource.id
        else:           
            data['resource_title'] = None
            data['resource_name'] = None
            data['resource_id'] = None
        if self.user:
            data['user_username'] = self.user.username
            data['user_id'] = self.user.id
        else:
            data['user_username'] = None
            data['user_id'] = None
        return data

    @classmethod
    def new_form_fields(cls):
        #fields = Resource.new_form_fields()
        fields = Resource.new_form_fields()
        del fields['name']
        del fields['title']
        fields.insert(0, 'resource', {'fieldLabel': 'Resource', 'xtype':'vault.resourcelinkfield'})
        return fields

    def _edit_form_fields(self):
        return self.new_form_fields()

    def _update_resource_id(self, asset_id):
        try:
            id = int(asset_id)
        except ValueError:
            return
        if id:
            self.resource = Session.query(Resource).filter(Resource.id==id).first()
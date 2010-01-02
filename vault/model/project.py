from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Project(Resource):
    __tablename__ = 'projects'

    # Relational
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'project'}

    # Data
    client = Column(String(255))
    
    def to_dict(self):
        data = Resource.to_dict(self)
        data['client'] = str(self.client)
        return data

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields.insert(2, ('client', 'Client'))
        return fields
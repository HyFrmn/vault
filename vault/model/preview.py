from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Preview(Resource):
    __tablename__ = 'previews'

    # Relational
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'preview'}

    # Data
    image = Column(String(255))
    
    def to_dict(self):
        data = Resource.to_dict(self)
        data['image'] = str(self.image)
        return data

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields.insert(2, ('image', 'Image', 'fileuploadfield'))
        return fields
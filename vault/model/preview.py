from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Preview(Resource):
    __tablename__ = 'previews'

    icon = '/icons/image.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'preview'}

    # Data
    image = Column(String(255))
    
    def to_dict(self):
        data = Resource.to_dict(self)
        data['image'] = str(self.image)
        return data

    def _update_image(self, image):
        self.image = str(image)

    @classmethod
    def new_form_fields(cls):
        fields = Resource.new_form_fields()
        fields.insert(2, 'image', { 'fieldLabel' : 'Image', 'xtype':'fileuploadfield'})
        return fields

    def _edit_form_fields(self, **kwargs):
        fields = Resource._edit_form_fields(self.__class__)
        del fields['image']
        return fields 

    @classmethod
    def _new_dialog_config(cls, *args, **kwargs):
        data = Resource._new_dialog_config(*args, **kwargs)
        data['fileUpload'] = True
        print data
        return data

#Black Magic
Resource._register(Preview)
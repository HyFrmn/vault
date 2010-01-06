import os
import subprocess

import pylons
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

    def _update_image(self, temppath):
        #Resize into web preview.
        print temppath
        image_path = os.path.join(pylons.config['uploads.previews'], os.path.basename(temppath))
        print image_path
        print image_path[len(pylons.config['uploads.root']):]
        params = { 'temppath' : temppath, 'fullpath' : image_path, 'width' : 600, 'height' : 400 }
        cmd = "convert %(temppath)s -resize %(width)dx%(height)d\> -size %(width)dx%(height)d xc:black +swap -gravity center -composite %(fullpath)s" % params
        subprocess.call(cmd, shell=True)
        self.image = str(image_path[len(pylons.config['uploads.root']):])

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
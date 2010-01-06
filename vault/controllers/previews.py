import os
import shutil
import logging
import subprocess

from pylons import request, response, session, config, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class PreviewsController(ResourcesController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')
    _poly_class_ = Preview
    
    def _before_create(self):
        permanent_store = config['uploads.previews']

        #Get Uploaded File
        type_ = self._poly_class_.__tablename__
        myfile = self.params[type_]['image']
        filepath = str(myfile.filename.lstrip(os.sep))
        fullpath = os.path.join(permanent_store, filepath)
        fullpath = os.path.splitext(fullpath)[0] + '.jpg'
        temppath = os.path.join('/tmp', os.path.basename(fullpath))
        permanent_file = open(temppath, 'w')
        log.info(myfile, permanent_file)
        shutil.copyfileobj(myfile.file, permanent_file)
        myfile.file.close()
        permanent_file.close()

        self.params[type_]['image'] = temppath
        return True

    def search_index(self):
        asset_id = self.params.get('parent_id', None)
        if asset_id:
            asset = meta.Session.query(Asset).filter(Asset.id==asset_id).first()
            if asset:
                c.resources = meta.Session.query(Preview).filter(Preview.id==asset.preview_id).all()
            else:
                c.resources = meta.Session.query(Preview).all()
            return c.resources
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

        #Resize into web preview.
        params = { 'temppath' : temppath, 'fullpath' : fullpath, 'width' : 600, 'height' : 400 }
        print params
        cmd = "convert %(temppath)s -resize %(width)dx%(height)d\> -size %(width)dx%(height)d xc:black +swap -gravity center -composite %(fullpath)s" % params
        subprocess.call(cmd, shell=True)
        os.remove(temppath)

        self.params[type_]['image'] = fullpath[len(config['uploads.root']):]
        return True
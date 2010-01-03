import os
import shutil
import logging

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
        myfile = self.params['preview']['image']
        print myfile.filename
        filepath = str(myfile.filename.lstrip(os.sep))
        fullpath = os.path.join(permanent_store, filepath)
        permanent_file = open(fullpath, 'w')
        log.info(myfile, permanent_file)
        shutil.copyfileobj(myfile.file, permanent_file)
        myfile.file.close()
        permanent_file.close()
        
        self.params['preview']['image'] = fullpath[len(config['uploads.root']):]
        return True
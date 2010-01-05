import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class VersionsController(ResourcesController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')
    _poly_class_ = Version

    def search_index(self):
        asset_id = self.params.get('parent_id', None)
        if asset_id:
            c.resources = meta.Session.query(Version).filter(Version.asset_id==int(asset_id)).all()
        else:
            c.resources = []
        print "Found the following versions:", c.resources, asset_id
        return c.resources
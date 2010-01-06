import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.controllers.xmlrpc import XMLRPCController

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class XmlrpcController(XMLRPCController, ResourcesController):
    def create_version(self, asset_id, preview_path, notes, metadata=None):
        asset = Asset.find(asset_id)
        if not asset:
            return ( False , "No asset found." )
        version_number = len(asset.versions) + 1
        
        #Setup Version Resource
        version = Version(description=notes,
                          title = "%s Version #%d" % (asset.title, version_number),
                          name = "%s_version_%d" % (asset.title, version_number))
        version.asset = asset
        meta.Session.add(version)
        meta.Session.commit()

        #Setup Preview Resource
        fullpath = preview_path
        preview = Preview(image=fullpath,
                          description="Preview for version [%s]" % version.name,
                          title = "%s Preview" % asset.title,
                          name = "%s_preview_%d" % (asset.name, version.id))
        meta.Session.add(preview)
        meta.Session.commit()

        version.preview = preview
        meta.Session.commit()
        return ( True , version.to_dict() )

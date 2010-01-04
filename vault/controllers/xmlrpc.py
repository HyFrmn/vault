import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.controllers.xmlrpc import XMLRPCController

from vault.lib.base import BaseController, render
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class XmlrpcController(XMLRPCController, ResourcesController):pass


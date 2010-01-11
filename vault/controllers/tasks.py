import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import *
from vault.controllers.resources import ResourcesController

log = logging.getLogger(__name__)

class TasksController(ResourcesController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('project', 'projects')
    _poly_class_ = Task
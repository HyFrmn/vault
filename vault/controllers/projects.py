import logging
import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.decorators import jsonify
from pylons.controllers.util import abort, redirect_to

from vault.lib.base import BaseController, render
import vault.model as model

log = logging.getLogger(__name__)

class ProjectsController(BaseController):

    def index(self, format='html'):
        q = model.meta.Session.query(model.Resource)
        c.projects = q.limit(5)
        
        if format in ['js','json']:
            #Render JSON
            response.headers['Content-Type'] = 'application/javascript'
            return self.to_json({'projects' : c.projects})
        return render("/project/index.html")

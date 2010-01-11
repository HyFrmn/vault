import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect, redirect_to

from vault.lib.base import *

log = logging.getLogger(__name__)

class LoginController(BaseController):
    def index(self):
        return self.login()
    
    def login(self):
        """
        Show login form. Submits to /login/submit
        """
        return render('login.mako')

    def submit(self):
        """
        Verify username and password
        """
        # Both fields filled?
        form_username = str(request.params.get('username'))
        form_password = str(request.params.get('password'))

        # Get user data from database
        db_user = meta.Session.query(User).filter(User.username==form_username).first()
        if db_user is None: # User does not exist
            return render('login.mako')

        # AUTHENTIC USER HERE
        #if db_user.passwd != md5.md5(form_password).hexdigest():
        #    return render('login.mako')

        # Mark user as logged in
        session['user'] = form_username
        session.save()

        # Send user back to the page he originally wanted to get to
        if session.get('path_before_login'):
            redirect_to(session['path_before_login'])
        else: # if previous target is unknown just send the user to a welcome page
            return redirect_to(controller='application', action='index')

    def logout(self):
        """
        Logout the user and display a confirmation message
        """
        if 'user' in session:
            del session['user']
            session.save()
        return render('login.mako')

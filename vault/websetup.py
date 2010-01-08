"""Setup the vault application"""
import os
import logging

from pylons import config

from vault.config.environment import load_environment
from vault.model import *

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup vault here"""
    load_environment(conf.global_conf, conf.local_conf)

    #Setup filesystem
    if not os.path.exists(config['uploads.previews']):
        os.mkdir(config['uploads.previews'])

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)

    #Setup Users for authentication.
    admin_user = User()
    admin_user.username = 'admin'
    meta.Session.add(admin_user)
    dummy_user = User()
    dummy_user.username = 'dummy'
    meta.Session.add(dummy_user)


    #Setup Defaults
    meta.Session.add(TaskTemplate(name="rough", title="Rough"))
    meta.Session.add(TaskTemplate(name="clean", title="Clean"))
    meta.Session.add(TaskTemplate(name="uv", title="UV"))
    meta.Session.add(TaskTemplate(name="texture", title="Texture"))
    meta.Session.add(TaskTemplate(name="hires", title="Hi Res Paint"))
    meta.Session.add(TaskTemplate(name="lowres", title="Low Res Paint"))
    meta.Session.add(TaskTemplate(name="layout", title="Layout"))
    meta.Session.add(TaskTemplate(name="light", title="Light"))
    meta.Session.add(TaskTemplate(name="texture_bake", title="Texture Bake"))
    meta.Session.add(TaskTemplate(name="animation", title="Animation"))
    meta.Session.add(TaskTemplate(name="rig", title="Rigging"))
    meta.Session.add(AssetTemplate(name="realtime_model", title="Realtime Model", meta={ 'tasks' : ['rough', 'clean', 'uv', 'texture']}))
    meta.Session.add(AssetTemplate(name="realtime_texture", title="Realtime Texture", meta={ 'tasks' : ['hires', 'lowres']}))
    meta.Session.add(AssetTemplate(name="realtime_layout", title="Realtime Layout", meta={ 'tasks' : ['layout', 'light', 'bake']}))
    meta.Session.commit()
    

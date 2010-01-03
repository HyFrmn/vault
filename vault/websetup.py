"""Setup the vault application"""
import os
import logging

from vault import config
from vault.config.environment import load_environment
from vault.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup vault here"""
    load_environment(conf.global_conf, conf.local_conf)

    #Setup filesystem
    os.mkdir(config['uploads.previews'])

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    
    

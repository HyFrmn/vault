"""The application's model objects"""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from vault.model import meta

__all__ = ['meta', 'Resource', 'Project', 'Preview', 'Asset', 'Task', 'Version']

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

from vault.model.resource import Resource, Connection
from vault.model.project import Project
from vault.model.preview import Preview
from vault.model.asset import Asset
from vault.model.task import Task
from vault.model.version import Version
from vault.model.asset_template import AssetTemplate

## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass

"""The application's model objects"""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from vault.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine

from vault.model.resource import Resource, Connection
from vault.model.project import Project
from vault.model.preview import Preview
from vault.model.asset import Asset
from vault.model.task import Task
from vault.model.version import Version
from vault.model.asset_template import AssetTemplate

AssetTemplate.assets = orm.relation(Asset, primaryjoin=AssetTemplate.id==Asset.template_id, foreign_keys=[Asset.template_id], remote_side=Asset.template_id)

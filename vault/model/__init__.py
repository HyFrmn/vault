"""The application's model objects"""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from vault.model import meta

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

resources_table = sa.Table("Resource", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True, autoincrement=True),
    sa.Column("name", sa.types.String(255), nullable=False),
    sa.Column("title", sa.types.String(255), nullable=False),
    sa.Column("description", sa.types.Text(), nullable=False),
    sa.Column("created", sa.types.DateTime(), nullable=False),
    sa.Column("modified", sa.types.DateTime(), nullable=False),
    )
#
class Resource(object):
    def __init__(self):
        now = datetime.datetime.now()
        self.created = now
        self.modified = now

    def __str__(self):
        return str(self.title)

    def to_dict(self):
        data = {}
        data['id'] = int(self.id)
        data['name'] = str(self.name)
        data['title'] = str(self.title)
        data['description'] = str(self.description)
        data['created'] = str(self.created)
        data['modified'] = str(self.modified)
        return data
    
    def to_json(self):
        return simplejson.dumps(self.to_dict())

orm.mapper(Resource, resources_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass

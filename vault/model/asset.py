from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Asset(Resource):
    __tablename__ = 'assets'

    # Inherit
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'asset'}

    # Relational 
    preview = Column(Integer, ForeignKey('resources.id'))
    status = Column(Integer)
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from resource import Resource

class Project(Resource):
    __tablename__ = 'projects'

    # Relational
    resource_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'project'}

    # Data
    client = Column(String(255))
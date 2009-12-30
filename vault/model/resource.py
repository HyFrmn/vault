import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from meta import Base

class Resource(Base):
    __tablename__ = 'resources'
    
    # Relational
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(30))
    __mapper_args__ = {'polymorphic_on' : type}
    
    # Data
    name = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    
    # Tracking
    created = Column(DateTime)
    modified = Column(DateTime)
    
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
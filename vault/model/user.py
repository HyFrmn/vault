import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from meta import Base

class User(Base):
    __tablename__ = 'users'

    # Relational
    id = Column(Integer, primary_key=True, autoincrement=True)
    #role = Column(Integer, ForeignKey('roles.id'))

    # Data
    username = Column(String(255))

    # Tracking
    last_login = Column(DateTime)

    def __init__(self):
        now = datetime.datetime.now()
        self.created = now
        self.modified = now

    def __str__(self):
        return str(self.title)

    def to_dict(self):
        data = {}
        data['id'] = int(self.id)
        data['role'] = int(self.role)
        data['username'] = str(self.username)
        data['last_login'] = self.last_login
        return data

    def to_json(self):
        return simplejson.dumps(self.to_dict())
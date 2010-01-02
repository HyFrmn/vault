import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation
from meta import Base

class Connection(Base):
    __tablename__ = 'connections'

    # Relational
    parent_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    child_id = Column(Integer, ForeignKey('resources.id'), primary_key=True)

    def __init__(self, parent_id, child_id):
        self.parent_id = parent_id
        self.child_id = child_id

class Resource(Base):
    __tablename__ = 'resources'
    
    icon = '/icons/page.png'
    
    # Relational
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(30))
    children = relation("Resource", Connection.__table__,
                        primaryjoin = id==Connection.__table__.c.parent_id,
                        secondaryjoin = Connection.__table__.c.child_id==id)
    __mapper_args__ = {'polymorphic_on' : type}
    
    # Data
    name = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    
    # Tracking
    created = Column(DateTime)
    modified = Column(DateTime)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
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
        data['type'] = str(self.__class__.__name__.lower())
        data['description'] = str(self.description)
        data['created'] = self.created
        data['modified'] = self.modified
        return data
    
    def to_json(self):
        return simplejson.dumps(self.to_dict())

    def _get_classname(self):
        return self.__class__.__name__.lower()
    _classname = property(_get_classname)

    @classmethod
    def new_form_fields(cls):
        return [('title', 'Title'),
                ('name', 'Name'),
                ('description', 'Description'),
                ('parent_id', 'Parent ID','hidden')]

    @classmethod
    def form_schema(cls, field_list, defaults):
        field_schemas = []
        for field in field_list:
            v = t_ = None
            if isinstance(field, (list, tuple)):
                f = field[0]
                if len(field) > 1:
                    t = field[1]
                    if len(field) > 2:
                        t_ = field[2]
                        if len(field) > 3:
                            v = field[3]
                else:
                    t = f
            else:
                t = f = field
            v = defaults.get(f, v)
            schema = cls.field_schema(f, t, t_, v)
            if schema:
                field_schemas.append(schema)
        return field_schemas

    @classmethod
    def field_schema(cls, field, title=None, type_=None, value=None):
        if not title:
            title = field
        if not type_:
            column_cls = getattr(cls, field).comparator.property.columns[0].type
            if isinstance(column_cls, Integer):
                type_ = 'numberfield'
            elif isinstance(column_cls, Text):
                print field, 'textarea'
                type_ = 'textarea'
            elif isinstance(column_cls, String):
                type_ = 'textfield'
        return { 'name' : '%s[%s]' % (cls.__name__.lower(), field), 'title' : title, 'type' : type_, 'value' : value }
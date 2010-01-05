import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relation
from meta import Base, Session

from UserDict import DictMixin


class odict(DictMixin):
    def __init__(self, data=None, **kwdata):
        self._keys = []
        self._data = {}
        if data is not None:
            if hasattr(data, 'items'):
                items = data.items()
            else:
                items = list(data)
            for i in xrange(len(items)):
                length = len(items[i])
                if length != 2:
                    raise ValueError('dictionary update sequence element '
                        '#%d has length %d; 2 is required' % (i, length))
                self._keys.append(items[i][0])
                self._data[items[i][0]] = items[i][1]
        if kwdata:
            self._merge_keys(kwdata.iterkeys())
            self.update(kwdata)

    
    def __repr__(self):
        result = []
        for key in self._keys:
            result.append('%s: %s' % (repr(key), repr(self._data[key])))
        return ''.join(['{', ', '.join(result), '}'])
    
    
    def _merge_keys(self, keys):
        self._keys.extend(keys)
        newkeys = {}
        self._keys = [newkeys.setdefault(x, x) for x in self._keys
            if x not in newkeys]
    
    
    def update(self, data):
        if data is not None:
            if hasattr(data, 'iterkeys'):
                self._merge_keys(data.iterkeys())
            else:
                self._merge_keys(data.keys())
            self._data.update(data)

    def insert(self, pos, key, value):
        self._keys.insert(pos, key)
        self._data[key] = value

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value
        
        
    def __getitem__(self, key):
        if isinstance(key, slice):
            result = [(k, self._data[k]) for k in self._keys[key]]
            return OrderedDict(result)
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)
        
        
    def keys(self):
        return list(self._keys)
    
    
    def copy(self):
        copyDict = odict()
        copyDict._data = self._data.copy()
        copyDict._keys = self._keys[:]
        return copyDict


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

    #Black Magic
    _classmap = {}

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
        if kwargs:
            self.update(kwargs)
        now = datetime.datetime.now()
        self.created = now
        self.modified = now

    @classmethod
    def _register(cls, class_):
        cls._classmap[class_.__tablename__] = class_

    def to_json(self):
        return simplejson.dumps(self.to_dict())

    def _get_classname(self):
        return self.__tablename__
    _classname = property(_get_classname)

    def __str__(self):
        return str(self.title)

    def update(self, kwargs):
        for k, v in kwargs.iteritems():
            update_attr_name = '_update_' + str(k)
            try:
                update_attr = getattr(self, update_attr_name)
                update_attr(v)
            except AttributeError:
                pass

    def to_dict(self):
        data = {}
        data['id'] = int(self.id)
        data['name'] = str(self.name)
        data['title'] = str(self.title)
        data['type'] = str(self.__tablename__)
        data['description'] = str(self.description)
        data['created'] = self.created
        data['modified'] = self.modified
        return data

    def _update_name(self, name):
        self.name = str(name)

    def _update_title(self, title):
        self.title = str(title)

    def _update_description(self, description):
        self.description = description

    @classmethod
    def new_dialog_config(cls, **kwargs):
        t = kwargs.get('type_')
        func = cls._classmap.get(t, cls)._dialog_config
        print func
        config = func(**kwargs)
        print config
        return config

    def edit_dialog_config(self, *args, **kwargs):
        config = self._dialog_config(self.id, edit=True,**kwargs)
        print config
        return config
        
    @classmethod
    def _dialog_config(cls, rid=None, edit=False, parent_id=None, title='New Resource', resultPanel='Vault.mainPanel', rtype=None, **kwargs):
        if not rtype:
            rtype = cls.__tablename__
        data = {
                'title' : title,
                'rid' : rid,
                'rtype' : rtype,
                'editForm' : edit,
                'resultPanel' : resultPanel,
            }
        if parent_id:
            data['storeParams'] = { 'parent_id' : parent_id }
        data.update(kwargs)
        print data
        return data

    def grid_config(self, **kwargs):
        data = {
            'xtype' : 'vault.grid',
            'rtype' : 'resources',
            'storeFields' : ['id', 'name', 'title', 'description', 'created', 'modified', 'type'],
            'storeRoot' : "resources",
            'title' : "Resources",
            'id' : '%s-grid' % self.__class__.__name__.lower(),
            'columns' : [self.config_grid_column('Title', 'title'),
                         self.config_grid_column('Type', 'type'),
                         self.config_grid_column('Created', 'created'),
                         self.config_grid_column('Description', 'description', sort=False)],
            }
        data.update(kwargs)
        return data

    @classmethod
    def config_grid_column(cls, label, field, width=200, sort=True):
        return { 'header': label, 'width' : width, 'dataIndex' : field, 'sortable' : sort}

    @classmethod
    def new_form_fields(cls):
        
        return odict([('title' , { 'fieldLabel': 'Title', 'enableKeyEvents' : True}),
                      ('name' , { 'fieldLabel' : 'Name'}),
                      ('description' , { 'fieldLabel' : 'Description', 'xtype' : 'textarea'}),
                      ('parent_id' , {'fieldLabel': 'Parent ID', 'xtype':'hidden'})])

    @classmethod
    def _edit_form_fields(cls, self=None):
        if not self:
            self = cls
        data = self.new_form_fields()
        del data['parent_id']
        data['name']['disabled'] = True
        data['_method'] = { 'xtype' : 'hidden', 'value' : 'PUT' }
        return data

    def edit_form_fields(self):
        data = self._edit_form_fields()
        for k, v in data.iteritems():
            try:
                data[k]['value'] = getattr(self, k)
            except AttributeError:
                pass
        return data

    @classmethod
    def form_schema(cls, field_defs, defaults=None):
        field_schemas = []
        for name, def_ in field_defs.iteritems():
            field = def_.copy()
            field['itemId'] = name
            if defaults:
                value = defaults.get(name)
                if value:
                    field['value'] = value
            if name != '_method':
                field['name'] = '%s[%s]' % (cls.__tablename__, name)
            else:
                field['name'] = name
            field_schemas.append(field)
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
        return { 'name' : '%s[%s]' % (cls.__tablename__, field), 'title' : title, 'type' : type_, 'value' : value }

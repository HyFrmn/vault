from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Time, Float
from sqlalchemy.orm import relation

from resource import Resource, odict, Session
from asset import Asset
from preview import Preview

class Version(Resource):
    __tablename__ = 'versions'

    icon = '/icons/pill.png'

    # Relational
    id = Column(Integer, ForeignKey('resources.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity' : 'versions'}

    # Data
    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relation(Asset, primaryjoin=asset_id==Asset.__table__.c.id, backref="versions")
    meta = Column(Text)
    parent_id = Column(Integer, ForeignKey('versions.id'))
    parent = relation("Asset", primaryjoin=parent_id==id)
    preview_id = Column(Integer, ForeignKey('previews.id'))
    preview = relation(Preview, primaryjoin=preview_id==Preview.__table__.c.id)

    def to_dict(self):
        data = Resource.to_dict(self)
        print 'Creating Dictionary for JSON output.'
        if self.asset:
            for k, v in self.asset.to_dict().iteritems():
                data['asset_' + k] = v
        return data

    @classmethod
    def new_form_fields(cls):
        #fields = Resource.new_form_fields()
        fields = Resource.new_form_fields()
        fields['asset'] = { 'fieldLabel' : 'Asset' , 'xtype' : 'vault.resourcelinkfield', 'rtype' : 'assets' }
        return fields

    def _edit_form_fields(self):
        return self.new_form_fields()

    def _update_asset_id(self, asset_id):
        try:
            id = int(asset_id)
        except ValueError:
            id = 0
        if id:
            asset = Session.query(Resource).filter(Resource.id==id).first()
            self.asset = asset

#Black Magic
Resource._register(Version)
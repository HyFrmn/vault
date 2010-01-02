//vim: ts=4:sw=4:nu:fdc=4:nospell
Vault.Details = Ext.extend(Ext.Panel, {

	// soft config (can be changed from outside)
	border:false,
	title: 'Details',
	storeUrl: '/resources.json',
	storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'image'],
	storeRoot: "resource",
	storeParams: {},
	title: "Resources",
	storeId: 0,
	autoScroll: true,

	template: new Ext.XTemplate(
			'<div class="details">',
			'<tpl for=".">',
			'<img src="{image}"><div class="details-info">',
			'<p>',
			'<b>Title:</b>',
			'<span>{title}</span>',
			'</p>',
			'<p>',
			'<b>Last Modified:</b>',
			'<span>{modified}</span></div>',
			'<p>{description}</p>',
			'</p>',
			'</div>',
			'</tpl>',
	'</div>'),

	initComponent:function(config) {
	// {{{
	// hard coded (cannot be changed from outside)
	var config = {
	};

	// apply config
	Ext.apply(this, config);
	Ext.apply(this.initialConfig, config);
	// }}}

	// call parent
	Vault.Details.superclass.initComponent.apply(this, arguments);

	// after parent code here, e.g. install event handlers
	this.store = new Ext.data.Store({
		proxy: new Ext.data.HttpProxy({
			url: this.storeUrl,
			method: 'GET',
		}),
		reader: new Ext.data.JsonReader({
			idProperty: 'id',
			fields: this.storeFields,
			root: this.storeRoot,
		}),
	}),
	this.store.load({
		params: this.storeParams,
		callback: this.updateDetails,
		scope: this,
	})
},

updateDetails: function(){
	detailsEl = this.body
	record = this.store.getById(this.storeId)
	if (record){
		this.template.overwrite(detailsEl, record.data)
		this.setTitle(record.data.title)
	}
},

onRender:function() {
	// call parent
	Vault.Details.superclass.onRender.apply(this, arguments);
}
});

//register xtype
Ext.reg('vault.details', Vault.Details); 

//eof
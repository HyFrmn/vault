//vim: ts=4:sw=4:nu:fdc=4:nospell
Vault.Details = Ext.extend(Ext.Panel, {

	// soft config (can be changed from outside)
	border:false,
	title: 'Details',
	rtype: 'resources',
	rid: 0,
	params: {},
	title: "Resources",
	storeId: 0,
	autoScroll: true,

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

	Ext.Ajax.request({
		params: this.params,
		success: this.success_callback,
		scope: this,
		url: '/' + this.rtype + '/' + this.rid + '.json'
	})
},

success_callback: function(response, result, type){
	console.info(response)
	obj = Ext.decode(response.responseText)
	detailsEl = this.body
	if (obj){
		tmpl = new Ext.XTemplate(obj.tmpl)
		tmpl.overwrite(detailsEl, obj.data)
		this.setTitle(obj.data.title)
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
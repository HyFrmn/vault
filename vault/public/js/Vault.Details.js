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
    	var config = {
    	};
    

    	Ext.apply(this, config);
    	Ext.apply(this.initialConfig, config);

    	Vault.Details.superclass.initComponent.apply(this, arguments);
    	this.listenTo = eval(this.listenTo)
    	if(this.listenTo){
    		this.listenTo.on(this.listenToEvent, function(record){
    			this.load_from_record(record)
    		}, this)
    	}
    	
    	if (this.rid != 0){
    		this.load_details(this.rtype,this.rid)
    	}
    },

    load_details: function(rtype, rid){
    	Ext.Ajax.request({
    		params: this.params,
    		success: this.success_callback,
    		scope: this,
    		url: '/' + rtype + '/' + rid + '.json'
    	})
    },
    
    load_from_record: function(record){
    	this.load_details(record.data.type, record.data.id)
    },
    
    success_callback: function(response, result, type){
    	obj = Ext.decode(response.responseText)
    	detailsEl = this.body
    	if (obj && detailsEl){
    		tmpl = new Ext.XTemplate(obj.tmpl)
    		tmpl.overwrite(detailsEl, obj.data)
    		this.setTitle(obj.data.title)
    		this.rid = obj.data.rid
    		this.rtype - obj.data.rtype
    	}
    },
});

Ext.reg('vault.details', Vault.Details);
Ext.ns("Vault")

Vault.SelectResourceDialog = Ext.extend(Vault.Dialog, {
	rtype: 'resources',
	rid: 1,
	storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'image'],
	storeParams: {},
	selected: null,
	callback: null,
	tpl: ['<tpl for=".">',
          '<div class="thumb-wrap" id="{name}">',
          '<div class="thumb"><img src="{image}" title="{name}"></div>',
          '<span class="x-editable">{title}</span></div>',
          '</tpl>',
          '<div class="x-clear"></div>'],
	initComponent: function(config){
	// Called during component initialization
		Ext.apply(this, config);
		Vault.SelectResourceDialog.superclass.initComponent.apply(this, arguments)
		this.addEvents("submitted")
		this.storeUrl = [this.rtype + '.json'].join('/')
		this.store = new Ext.data.Store({
			proxy: new Ext.data.HttpProxy({
				url: this.storeUrl,
				method: 'GET',
			}),
			reader: new Ext.data.JsonReader({
				idProperty: 'name',
				root: this.rtype,
				fields: this.storeFields,
			})
		})
		this.view = new Ext.DataView({
	        store: this.store,
	        tpl:  new Ext.XTemplate(this.tpl),
	        autoHeight:true,
	        multiSelect: true,
	        overClass:'x-view-over',
	        itemSelector:'div.thumb-wrap',
	        emptyText: 'No images to display',
	        singleSelect: true,
	        multiSelect: false,
	    })
		this.details = new Vault.Details()
		this.search_field = new Ext.form.TextField({ enableKeyEvents: true})
        this.search_field.on("keyup", function(){
          filter = this.search_field.getValue()
          xpr = new RegExp(filter)
          this.store.filter('name', xpr)
        },this)
		this.add({
				layout: 'border',
				items: [{
					     region: 'center',
					     autoScroll: true,
					     items: this.view,
					     border: false,
					},{
						region: 'east',
						items: this.details,
						width: '150',
						layout: 'fit',
						split: true,
					},{
						region: 'north',
						xtype: 'toolbar',
						height: 32,
						items: [{
							xtype: 'tbfill'
						  }, this.search_field]
					}],
				buttons: [{ 
							text : 'Select',
							handler: function(){
								this.submit()
							},
							scope: this,
						},{
							text:'Cancel',
							'handler' : function(){
								this.close()
							},
							scope: this,
						}],
				})
		this.store.load({
			params: this.storeParams,
			scope: this,
		})
		this.view.on("selectionchange", function(selection){
			record = this.view.getSelectedRecords()[0]
			if (record){
				this.selected = record
				this.details.update_details(record.data.type, record.data.id)
			}
		}, this)
	},
	submit: function(){
		if (this.callback){
			this.callback.apply(this.scope, [this, this.selected])
		}
		this.close()
		this.fireEvent("submitted", this.selected)
	}
})
Ext.reg('vault.selectresourcedialog', Vault.SelectResourceDialog)
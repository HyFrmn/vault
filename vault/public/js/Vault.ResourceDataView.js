Ext.ns("Vault")

Vault.ResourceDataView = Ext.extend(Ext.Panel, {
	rtype: 'resources',
	rid: 1,
	storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'preview_image'],
	storeParams: {},
	selected: null,
	callback: null,
	border: false,
	layout: 'border',
	tbarItems: [],
	tpl: ['<tpl for=".">',
          '<div class="thumb-wrap" id="{name}">',
          '<div class="thumb"><img src="{preview_image}" title="{name}"></div>',
          '<span class="x-editable">{title}</span></div>',
          '</tpl>',
          '<div class="x-clear"></div>'],
	initComponent: function(config){
	// Called during component initialization
		Ext.apply(this, config);
		Vault.ResourceDataView.superclass.initComponent.apply(this, arguments)
		this.addEvents("selectionchange")
        this.enableBubble("selectionchange")
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
		this.tbarItems.push({ xtype: 'tbfill' })
		this.tbarItems.push(this.search_field)
		this.search_field.on("keyup", function(){
		  filter = this.search_field.getValue()
		  xpr = new RegExp(filter.toLowerCase())
		  this.store.filter('name', xpr)
		},this)
		this.add({
					region: 'center',
					autoScroll: true,
					items: this.view,
					border: false,
				},{
					region: 'east',
					items: this.details,
					width: '250',
					layout: 'fit',
					split: true,
					border:false,
					autoScroll: true,
				},{
					region: 'north',
					height: 32,
					xtype: 'toolbar',
					items: this.tbarItems,
				})
		this.store.load({
			params: this.storeParams,
		})
		this.view.on("selectionchange", function(selection){
			record = this.view.getSelectedRecords()[0]
			if (record){
				this.selected = record
				this.details.load_from_record(record)
                this.fireEvent("selectionchange", record)
			}
		}, this)
	},
	
    getSelected: function(){
	   return this.selected
    },
})
Ext.reg('vault.resourcedataview', Vault.ResourceDataView)
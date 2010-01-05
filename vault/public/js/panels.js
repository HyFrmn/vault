Ext.ns("Vault")

Vault.newResourceGrid = function(params, config){
	grid = new Vault.Grid(Ext.apply({
			storeUrl: '/resources.json',
			storeParams: params,
			storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type'],
			storeRoot: "resource",
			title: "Resources",
			columns: [	{header: 'Title', width: 200, sortable: true, dataIndex: 'title'},
			          	{header: 'Type', width: 200, sortable: true, dataIndex: 'type'},
			          	{header: 'Created', width: 100, sortable: true, dataIndex: 'created'},
			          	{header: 'Description', dataIndex: 'description'}],
			tbar: [{
					text: 'Add Resource',
					handler: function(){
						Vault.newResourceForm(Vault.mainPanel, 1)
					},
					scope: this,
			 },{
					text: 'Add Preview',
					handler: function(){
						Vault.newPreviewForm(Vault.mainPanel, 1)
					},
					scope: this,
			 },{
					text: 'Add Asset',
					handler: function(){
						Vault.newResourceForm(Vault.mainPanel, project_id)
					},
					scope: this,
			 }]
	}, config))
	return grid
}

Vault.ResourceDataView = Ext.extend(Ext.Panel, {
	rtype: 'resources',
	rid: 1,
	storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'preview_image'],
	storeParams: {},
	selected: null,
	callback: null,
	border: false,
	layout: 'border',
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
		this.details = new Vault.Details({listenTo: this})
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
					})
				
		console.info("Loading " + this.storeUrl)
		this.store.load({
			params: this.storeParams,
		})
		this.view.on("selectionchange", function(selection){
			record = this.view.getSelectedRecords()[0]
			if (record){
				this.selected = record
				this.fireEvent("selectionchange", record)
			}
			
		}, this)
	},
	
getSelected: function(){
	return this.selected
},
})
Ext.reg('vault.resourcedataview', Vault.ResourceDataView)
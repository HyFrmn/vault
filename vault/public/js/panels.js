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
						Vault.newResourceForm(Vault.mainPanel, project_id)
					},
					scope: this,
			 }]
	}, config))
	return grid
}

Vault.newResourceDetails = function(id, config){
	// soft config (can be changed from outside)
	details = new Vault.Details(Ext.apply({
		storeParams: { resource_id : id},
		storeId: id,
	}, config))
	return details
}
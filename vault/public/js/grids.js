Ext.ns("Vault");

Vault.Grid = Ext.extend(Ext.grid.GridPanel, {
 
    // soft config (can be changed from outside)
    border:false,
    storeUrl: '/resources.json',
    storeParams: {},
    storeFields: ['id', 'name', 'title', 'description', 'created', 'modified'],
    storeRoot: "resource",
    parentId: null,
    title: "Resources",
    resultPanel: "Vault.mainPanel",
    columns: [{header: 'Title', width: 200, sortable: true, dataIndex: 'title'},
    {header: 'Created', width: 100, sortable: true, dataIndex: 'created'},
    {header: 'Description', dataIndex: 'description'}],

	colModel: new Ext.grid.ColumnModel({
        defaults: {
            width: 120,
            sortable: true,
        },
        columns: this.columns,
    }),

    
    sm: new Ext.grid.RowSelectionModel({
    	
    }),
    
    listeners:{
		rowdblclick: function( gridObj, rowIndex, event) {
			record = this.store.getAt(rowIndex);
			console.info(record)
			console.info(this.resultPanel)
			if (this.resultPanel){
				this.resultPanel.replace({ xtype: 'vault.details', rid: record['id']})
			}
	}
	},

    initComponent:function(config) {

        var config = {
        };
 
        // apply config
        Ext.apply(this, config);
        Ext.apply(this.initialConfig, config);
 
        // call parent
        Vault.Grid.superclass.initComponent.apply(this, arguments);
 
        // after parent code here, e.g. install event handlers
		this.store = new Ext.data.Store({
			proxy: new Ext.data.HttpProxy({
				url: this.storeUrl,
				baseParams: this.storeParams,
				method: 'GET',
			}),
			reader: new Ext.data.JsonReader({
				idProperty: 'id',
				fields: this.storeFields,
				root: this.storeRoot,
			}),
		})
		this.resultPanel = eval(this.resultPanel)
		console.info(this.resultPanel)
    },

    onRender:function() {
 
        // before parent code
        this.store.url = this.storeUrl
 		this.store.load({
 			params:this.storeParams
 		})
        // call parent
        Vault.Grid.superclass.onRender.apply(this, arguments);
 
        // after parent code, e.g. install event handlers on rendered components
 
    } // eo function onRender

 
    // any other added/overrided methods
}); // eo extend
 
// register xtype
Ext.reg('vault.grid', Vault.Grid); 

// eof
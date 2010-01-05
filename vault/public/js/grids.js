Ext.ns("Vault");

Vault.Grid = Ext.extend(Ext.grid.GridPanel, {
    // soft config (can be changed from outside)
    border:false,
    searchParams: {},
    storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type'],
    rtype: "resources",
    listenTo: null,
    listenToEvent: "selectionchange",
    title: "Resources",
    resultPanel: null,
    selectedRow: null,
    columns: [{header: 'Title', width: 200, sortable: true, dataIndex: 'title'},
              {header: 'Type', width: 200, sortable: true, dataIndex: 'type'},
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
    	singleSelect: true,
    }),
    viewConfig: {
    	forceFit: true
    },
    initComponent:function(config) {

        var config = {
        };
 
        // apply config
        Ext.apply(this, config);
        Ext.apply(this.initialConfig, config);
        // call parent
        Vault.Grid.superclass.initComponent.apply(this, arguments);
        this.sm.on("rowselect", function(sm, index, record) {
    			resultPanel = eval(this.resultPanel)
    			if (resultPanel){
    				resultPanel.replace({ xtype: 'vault.details', rid: record['id'], rtype: record.data.type})
    			}
    		}, this)

        this.listenTo = eval(this.listenTo)
        if(this.listenTo){
            this.listenTo.on(this.listenToEvent, function(record){
                this.update_from_record(record)
        }, this)
        }

        // after parent code here, e.g. install event handlers
		this.store = new Ext.data.Store({
			proxy: new Ext.data.HttpProxy({
				url: this.getUrl(),
				baseParams: this.storeParams,
				method: 'GET',
			}),
			reader: new Ext.data.JsonReader({
				idProperty: 'id',
				fields: this.storeFields,
				root: this.rtype,
			}),
		})
 		this.store.load({
 			params:this.searchParams
 		})
    },

    update_from_record: function(record){
		this.store.load({
			params: { parent_id: record.data.id }
		})
	},

    getSelected: function(){
        return this.sm.getSelected()
    },

    getUrl: function(){
        return ("/" + this.rtype + ".json")
    }
})
// register xtype
Ext.reg('vault.grid', Vault.Grid); 

// eof
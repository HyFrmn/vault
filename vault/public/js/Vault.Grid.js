Ext.ns("Vault");

Vault.Grid = Ext.extend(Ext.grid.GridPanel, {
    // soft config (can be changed from outside)
    border:false,
    searchParams: { start:0, limit:25 },
    storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type'],
    rtype: "resources",
    title: "Resources",
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

        var config = {
            tbar: [Vault.Actions.addComment,],
            bbar: new Ext.PagingToolbar({
                displayInfo: true,
                pageSize: 25,
                prependButtons: true,
                store: this.store
        })

            
        };
 
        // apply config
        Ext.apply(this, config);
        Ext.apply(this.initialConfig, config);
        // call parent
        Vault.Grid.superclass.initComponent.apply(this, arguments);
        this.addEvents("selectionchange")
        this.enableBubble("selectionchange")
        this.sm.on("rowselect", function(sm, index, record) {
                this.selected = record
    			this.fireEvent("selectionchange", record)
    		}, this)

        // after parent code here, e.g. install event handlers

 		this.store.load({
 			params:this.searchParams
 		})
    },

    getSelected: function(){
        return this.sm.getSelected()
    },

    getUrl: function(){
        return ("/" + this.rtype + ".json")
    },
})
// register xtype
Ext.reg('vault.grid', Vault.Grid); 

// eof
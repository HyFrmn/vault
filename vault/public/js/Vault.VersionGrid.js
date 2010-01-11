Ext.ns("Vault");

Vault.VersionGrid = Ext.extend(Vault.Grid, {
    // soft config (can be changed from outside)
    storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'preview_image'],
    rtype: "versions",
    title: "Versions",
    selectedRow: null,
    columns: [{header: 'Title', width: 200, sortable: true, dataIndex: 'title'},
              {header: 'Preview', width: 200, sortable: true, dataIndex: 'preview_image'},
              {header: 'Type', width: 200, sortable: true, dataIndex: 'type'},
              {header: 'Created', width: 100, sortable: true, dataIndex: 'created'},
              {header: 'Description', dataIndex: 'description'}],
    initComponent:function(config) {
        Vault.VersionGrid.superclass.initComponent.apply(this, arguments);
    },
})
// register xtype
Ext.reg('vault.versiongrid', Vault.VersionGrid); 

// eof
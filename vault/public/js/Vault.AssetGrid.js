Ext.ns("Vault");

Vault.AssetGrid = Ext.extend(Vault.Grid, {
    // soft config (can be changed from outside)
    storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'preview_image', 'template_name', 'template_title'],
    rtype: "assets",
    title: "Assets",
    selectedRow: null,
    columns: [{header: 'Title', width: 200, sortable: true, dataIndex: 'title'},
              {header: 'Preview', width: 200, sortable: true, dataIndex: 'preview_image'},
              {header: 'Template', width: 200, sortable: true, dataIndex: 'template_title'},
              {header: 'Type', width: 200, sortable: true, dataIndex: 'type'},
              {header: 'Created', width: 100, sortable: true, dataIndex: 'created'},
              {header: 'Description', dataIndex: 'description'}],
    initComponent:function(config) {
        Vault.AssetGrid.superclass.initComponent.apply(this, arguments);
    },
})
// register xtype
Ext.reg('vault.assetgrid', Vault.AssetGrid); 

// eof
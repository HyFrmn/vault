Ext.ns("Vault");

Vault.CommentGrid = Ext.extend(Vault.Grid, {
    // soft config (can be changed from outside)
    storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'resource_name', 'resource_title','resource_id', 'user_id','user_username',],
    rtype: "comments",
    title: "Comments",
    selectedRow: null,
    columns: [{header: 'Resource', width: 200, sortable: true, dataIndex: 'resource_title'},
              {header: 'User', width: 200, sortable: true, dataIndex: 'user_username'},
              {header: 'Comment', width: 100, sortable: true, dataIndex: 'description'},
              {header: 'Date', dataIndex: 'created'}],
    initComponent:function(config) {
        Vault.CommentGrid.superclass.initComponent.apply(this, arguments);
    },
})
// register xtype
Ext.reg('vault.commentgrid', Vault.CommentGrid); 

// eof
/**
 * @author mpeter
 */

Ext.ns("Vault.Actions")

Vault.Actions.addComment = new Ext.Action({
    text: 'Add Comment',
    handler: function(){
        record = Vault.app.getSelected()
        if (record){
            dialog = new Vault.RestfulFormDialog({ rtype: 'comments', storeParams: {
                resource_id: record.data.id,
            }})
            dialog.show()
        }
    }
})

Vault.Actions.newAsset = new Ext.Action({
    text: 'New Asset',
    handler: function(){
        dialog = new Vault.RestfulFormDialog({ rtype: 'assets', storeParams: {
            project_id: Vault.app.getProject(),
        }})
        dialog.show()
    }
})
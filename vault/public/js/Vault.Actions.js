/**
 * @author mpeter
 */

Ext.ns("Vault.Actions")

Vault.Actions.addComment = new Ext.Action({
    text: 'Add Comment',
    handler: function(){
        record = Vault.app.getSelected()
        if (record){
            dialog = new Vault.RestfulFormDialog({ title: 'Add Comment', rtype: 'comments', storeParams: {
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

Vault.Actions.addCommentButton = Ext.extend(Ext.Button, {
    text: 'Add Comment',
    handler: function(b, e){
        parent = b.findParentBy(function(container, this_component){
            func = container['getSelected']
            if (func){
				return true
			}
			return false
        })
        record = Vault.app.getSelected()
        if (record){
            dialog = new Vault.RestfulFormDialog({ title: 'Add Comment', rtype: 'comments', storeParams: {
                resource_id: record.data.id,
            }})
            dialog.show()
        }
    }
})
Ext.reg('vault.addcommentbutton', Vault.Actions.addCommentButton)

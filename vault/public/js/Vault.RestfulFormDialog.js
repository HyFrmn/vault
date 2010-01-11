/**
 * @author mpeter
 */

Ext.ns("Vault")

Vault.RestfulFormDialog = Ext.extend(Vault.FormDialog, {
    rtype: 'resources',
    rid: 1,
    initComponent: function(config){
    // Called during component initialization
        Ext.apply(this, config);
        if (this.editForm){
            this.storeUrl = [this.rtype, this.rid, 'edit.json'].join('/')
            this.submitUrl = [this.rtype, this.rid].join('/')
        } else {
            this.storeUrl = [this.rtype, 'new.json'].join('/')
            this.submitUrl = [this.rtype].join('/')
        }
        Vault.RestfulFormDialog.superclass.initComponent.apply(this, arguments)
    },
})

Ext.reg('vault.restfulformdialog', Vault.RestfulFormDialog)

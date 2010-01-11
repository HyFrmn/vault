/**
 * @author mpeter
 */

Ext.ns("Vault")

Vault.close_window_callback = function(o){
    win = o.findParentByType(Ext.Window)
    win.close()
}

Vault.Dialog = Ext.extend(Ext.Window, {
    // Prototype Defaults, can be overridden by user's config object
    title: 'Dialog',
    closable: true,
    plain: true,
    layout: 'fit',

    width: 600,
    height: 300,

    initComponent: function(config){
        Ext.apply(this, {
        
        });
        Vault.Dialog.superclass.initComponent.apply(this, arguments);
    }
});

//register xtype to allow for lazy initialization
Ext.reg('vault.dialog', Vault.Dialog);
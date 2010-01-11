/**
 * @author mpeter
 */
Ext.ns("Vault")

Vault.LayoutPanel = Ext.extend(Ext.Panel, {
    // Prototype Defaults, can be overridden by user's config object
    layout: 'fit',
    
    initComponent: function(arguments){
        Ext.apply(this, {
        });
        Vault.LayoutPanel.superclass.initComponent.apply(this, arguments);
    },

    replace: function(panel){
        this.removeAll()
        this.add(panel)
        this.doLayout()
    },
    
    loadLayout : function(params){
        Ext.Ajax.request({
           url: 'views.json',
           success: this.loadLayout_callback,
           scope: this,
           params: {
               'my-header': 'foo',
           },
           params: params,
           method: 'GET',
        })
    },

    loadLayout_callback : function(r, o){
        obj = Ext.decode(r.responseText)
        panel = new Vault.LayoutPanel({items: obj})
        this.replace(panel)
    },
});

//register xtype to allow for lazy initialization
Ext.reg('vault.layoutpanel', Vault.LayoutPanel);
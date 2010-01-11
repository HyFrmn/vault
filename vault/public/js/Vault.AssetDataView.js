Ext.ns("Vault")

Vault.AssetDataView = Ext.extend(Vault.ResourceDataView, {
	rtype: 'assets',
	rid: 1,
    tbarItems: [ Vault.Actions.newAsset, new Vault.Actions.addCommentButton],
	storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type',
                  'preview_image', 'preview_name', 'preview_title'],
	tpl: ['<tpl for=".">',
          '<div class="thumb-wrap" id="{name}">',
          '<div class="thumb"><img src="{preview_image}" title="{name}"></div>',
          '<span class="x-editable">{title}</span></div>',
          '</tpl>',
          '<div class="x-clear"></div>'],
	initComponent: function(config){
        // Called during component initialization
        Ext.apply(this, config);
        Vault.AssetDataView.superclass.initComponent.apply(this, arguments)
    },
})
Ext.reg('vault.assetdataview', Vault.AssetDataView)
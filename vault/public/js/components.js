//vim: ts=4:sw=4:nu:fdc=4:nospell
Vault.OpenFormDialogButton = Ext.extend(Ext.Button, {
	// soft config (can be changed from outside)
	text: 'Open Dialog',
	dialogConfig: {},
	parentPanel: null,
	resultPanel: this.resultPanel,
	initComponent:function(config) {

		// apply config
		Ext.apply(this, config);
		Ext.apply(this.initialConfig, config);
	
		// call parent
		Vault.Details.superclass.initComponent.apply(this, arguments);
	
		this.on("click", function(){
			config = this.dialogConfig
			console.info(config)
			cmp = Ext.getCmp(this.parentPanel)
			dynamic = {}
			if (cmp){
				record = cmp.getSelected()
				rid = record.data.id
				config = Ext.apply(config, { rid: rid, rtype: 'resources' })
			}
			console.info(config)
			dialog = new Vault.RestfulFormDialog(config)
			dialog.show()
		}, this)
	},
})

//register xtype
Ext.reg('vault.open_form_dialog_button', Vault.OpenFormDialogButton); 

//eof
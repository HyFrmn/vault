//vim: ts=4:sw=4:nu:fdc=4:nospell
Vault.OpenFormDialogButton = Ext.extend(Ext.Button, {
	// soft config (can be changed from outside)
	text: 'Open Dialog',
	dialogConfig: {},
	resultPanel: this.resultPanel,
	initComponent:function(config) {

		// hard coded (cannot be changed from outside)
		var config = {
		};

		// apply config
		Ext.apply(this, config);
		Ext.apply(this.initialConfig, config);
	
		// call parent
		Vault.Details.superclass.initComponent.apply(this, arguments);
	
		this.on("click", function(){
			dialog = new Vault.FormDialog(this.dialogConfig)
			console.info(dialog)
			dialog.show()
		}, this)
	},
})

//register xtype
Ext.reg('vault.open_form_dialog_button', Vault.OpenFormDialogButton); 

//eof
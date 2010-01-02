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

	width: 400,
	height: 300,

	initComponent: function(config){
	// Called during component initialization

	// Config object has already been applied to 'this' so properties can 
	// be overriden here or new properties (e.g. items, tools, buttons) 
	// can be added, eg:
	Ext.apply(this, {
		
	});

	// Before parent code

	// Call parent (required)
	Vault.Dialog.superclass.initComponent.apply(this, arguments);

	// After parent code
	// e.g. install event handlers on rendered component
},

});

//register xtype to allow for lazy initialization
Ext.reg('vault.dialog', Vault.Dialog);

Vault.FormDialog = Ext.extend(Vault.Dialog, {
	// Prototype Defaults, can be overridden by user's config object
	title: 'Form Dialog',
	storeUrl: null,
	storeParams: null,
	submitUrl: null,
	standardSubmit: false,
	resultPanel: null,
	defaultValues:{},
	initComponent: function(config){
	// Called during component initialization
	this.store = new Ext.data.Store({
		
		proxy: new Ext.data.HttpProxy({
			url: this.storeUrl,
			method: 'GET',
		}),
		reader: new Ext.data.JsonReader({
			idProperty: 'name',
			fields: ['name', 'type', 'title', 'value'],
		})
	})
	console.info(this.defaultValues)
	this.form = new Ext.FormPanel({
		frame: true,
		bodyStyle: 'padding:5px 5px 0',
		url: this.submitUrl,
		method: 'POST',
		standardSubmit: this.standardSubmit,
		defaults: {
			width: 250
		},
		defaultType: 'textfield',
		buttons: [{
			text: 'Save',
			handler: function(){
				this.form.getForm().submit({
					params: this.form.getForm().getValues(),
					success: function(){
						this.load_results()
					},
					failure: function(f, a){
						alert(a.failureType)
					},
					scope: this
				})
				this.close()
			},
			scope: this
		},{
			text: 'Cancel',
			handler: this.close,
			scope: this
		}]
	});

	
	// Config object has already been applied to 'this' so properties can 
	// be overriden here or new properties (e.g. items, tools, buttons) 
	// can be added, eg:
	Ext.apply(this, {
		items: this.form,
	});

	// Before parent code

	// Call parent (required)
	Vault.FormDialog.superclass.initComponent.apply(this, arguments);

	// After parent code
	// e.g. install event handlers on rendered component
	},

	show: function(arguments){
		this.store.load({
			params: this.storeParams,
			callback: this.load_callback,
			scope: this,
			})
	},

	load_callback: function(arguments){
		console.info('Adding Form Fields. ' + this.store.getCount())
		
		this.store.each(function(r){
			this.form.add({
				name: r.data.name,
				fieldLabel: r.data.title,
				xtype: r.data.type,
				value: r.data.value
			})
		}, this)
		
	Vault.FormDialog.superclass.show.apply(this)
	},
	
	load_results: function(){
		if (this.resultPanel){
			this.resultPanel.removeAll()
			this.resultPanel.add(new Vault.Details())
			this.resultPanel.doLayout()
		}
	}
});

//register xtype to allow for lazy initialization
Ext.reg('vault.formdialog', Vault.FormDialog);

Vault.newResourceForm = function(resultPanel, parent_id){
	dialog = new Vault.FormDialog({
		title: 'New Resource',
		storeUrl: '/resources/new.json',
		storeParams: { parent_id: parent_id },
		submitUrl: '/resources',
		resultPanel: resultPanel,
			})
	dialog.show()
}

Vault.newProjectForm = function(resultPanel){
	dialog = new Vault.FormDialog({
		title: 'New Project',
		storeUrl: '/projects/new.json',
		submitUrl: '/projects',
		resultPanel: resultPanel,
			})
	dialog.show()
}
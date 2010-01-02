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
	fileUpload: false,
	
	initComponent: function(config){
	// Called during component initialization
		Ext.apply(this, config);
		
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
	this.form = new Ext.FormPanel({
		url: this.submitUrl,
		method: 'POST',
		defaults: {
			width: 250
		},
		defaultType: 'textfield',
		fileUpload: true,
		buttons: [{
			text: 'Save',
			handler: function(){
				if (this.fileUpload){
					Ext.Ajax.request({
						form : this.form.getForm().getEl().dom,
						url: this.submitUrl,
						method: 'POST',
						isUpload: this.fileUpload,
						success: this.load_results,
						failure: alert,
						scope: this,
					})
					this.close()
				} else {
					this.form.getForm().submit({
						method: 'POST',
						url: this.submitUrl,
						success: this.load_results,
						failure: alert,
						scope: this,
						params: this.form.getForm().getValues(),
						})
				}
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
		items: new Ext.Panel( {
			plain: true,
			layout: 'fit',
			items: this.form,
			frame: true,
			bodyStyle: 'padding:5px 5px 0',
			}),
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
		this.title_field = null
		this.name_field = null
		
		xpr = /(\w+)\[(\w+)\]/
		this.form.removeAll()
		cmpindex = 0
		this.store.each(function(r){
			match = xpr.exec(r.data.name)
			if (match){
				obj = match[1]
				field = match[2]
			} else {
				field = r.data.name
			}
			this.form.add({
				name: r.data.name,
				fieldLabel: r.data.title,
				xtype: r.data.type,
				value: r.data.value,
				enableKeyEvents: true,
				itemId: field,
			})
			
			if (field=='title'){
				this.title_field = this.form.getComponent(field)
			}
			if (field=='name'){
				this.name_field = this.form.getComponent(field)
			}
			
		}, this)
		if (this.name_field && this.title_field){
			this.title_field.on('keyup',function(){
                title = this.title_field.getValue(),
                name = title.toLowerCase()
                name = name.replace(/ /g, '_')
                re = /[^a-z_]/g
                name = name.replace(re, '')
                this.name_field.setValue(name)
            },
            this)
		}
		
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

Vault.newPreviewForm = function(resultPanel, parent_id){
	dialog = new Vault.FormDialog({
		title: 'New Preview',
		storeUrl: '/previews/new.json',
		submitUrl: '/previews.json',
		storeParams: { parent_id: parent_id },
		resultPanel: resultPanel,
		fileUpload: true,
			})
		
	dialog.show()
}
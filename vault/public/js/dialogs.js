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
	editForm: false,
	waitMsg: "Contacting Server.",
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
				fields: ['name', 'fieldLabel', 'xtype', 'value', 'itemId', 'enableKeyEvents', 'rtype', {name: 'disabled', defaultValue: false}],
			})
	})
		
		
	this.form = new Ext.FormPanel({
		url: this.submitUrl,
		method: 'POST',
		defaults: {
			width: 250
		},
		defaultType: 'textfield',
		fileUpload: false,
		buttons: [{
			text: 'Save',
			handler: function(){
				if (this.fileUpload){
					Ext.Ajax.request({
						form : this.form.getForm().getEl().dom,
						url: this.submitUrl,
						method: 'POST',
						isUpload: this.fileUpload,
						success: this.ajax_submit_success_callback,
						failure: alert,
						scope: this,
						waitMsg: this.waitMsg,
					})
					this.close()
				} else {
					this.form.getForm().submit({
						method: 'POST',
						url: this.submitUrl,
						success: this.form_submit_success_callback,
						failure: alert,
						scope: this,
						params: this.form.getForm().getValues(),
						waitMsg: this.waitMsg,
					})
				}
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
		file_xpr = /file/
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
			
			this.form.add(r.data)
			if (field=='title'){
				this.title_field = this.form.getComponent(field)
			}
			if (field=='name'){
				this.name_field = this.form.getComponent(field)
			}
			if (file_xpr.test(r.data.xtype)){
				this.fileUpload = true
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
		this.resultPanel = eval(this.resultPanel)
	},
	
	ajax_submit_success_callback: function(response, options){
		obj = Ext.decode(response.responseText)
		this.switch_view(obj)
	},

	form_submit_success_callback: function(response, result, type){
		obj = Ext.decode(result.response.responseText)
		this.switch_view(obj)
	},
	
	switch_view: function(obj){
		this.close()
		if (this.resultPanel){
			this.resultPanel.removeAll()
			this.resultPanel.add(obj.view)
			this.resultPanel.doLayout()
		}
	},
});

//register xtype to allow for lazy initialization
Ext.reg('vault.formdialog', Vault.FormDialog);

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

//register xtype to allow for lazy initialization
Ext.reg('vault.formdialog', Vault.FormDialog);

Vault.SelectResourceDialog = Ext.extend(Vault.Dialog, {
	rtype: 'resources',
	rid: 1,
	storeFields: ['id', 'name', 'title', 'description', 'created', 'modified', 'type', 'image'],
	storeParams: {},
	selected: null,
	callback: null,
	tpl: ['<tpl for=".">',
          '<div class="thumb-wrap" id="{name}">',
          '<div class="thumb"><img src="{image}" title="{name}"></div>',
          '<span class="x-editable">{title}</span></div>',
          '</tpl>',
          '<div class="x-clear"></div>'],
	initComponent: function(config){
	// Called during component initialization
		Ext.apply(this, config);
		Vault.SelectResourceDialog.superclass.initComponent.apply(this, arguments)
		this.addEvents("submitted")
		this.storeUrl = [this.rtype + '.json'].join('/')
		this.store = new Ext.data.Store({
			proxy: new Ext.data.HttpProxy({
				url: this.storeUrl,
				method: 'GET',
			}),
			reader: new Ext.data.JsonReader({
				idProperty: 'name',
				root: this.rtype,
				fields: this.storeFields,
			})
		})
		this.view = new Ext.DataView({
	        store: this.store,
	        tpl:  new Ext.XTemplate(this.tpl),
	        autoHeight:true,
	        multiSelect: true,
	        overClass:'x-view-over',
	        itemSelector:'div.thumb-wrap',
	        emptyText: 'No images to display',
	        singleSelect: true,
	        multiSelect: false,
	    })
		this.details = new Vault.Details()
		this.add({
				layout: 'border',
				items: [{
					region: 'center',
					autoScroll: true,
					items: this.view,
					border: false,
					},{
						region: 'east',
						items: this.details,
						width: '150',
						layout: 'fit',
						split: true,
					}],
				buttons: [{ 
							text : 'Select',
							handler: function(){
								this.submit()
							},
							scope: this,
						},{
							text:'Cancel',
							'handler' : function(){
								this.close()
							},
							scope: this,
						}],
				})
		this.store.load({
			params: this.storeParams,
			scope: this,
		})
		this.view.on("selectionchange", function(selection){
			record = this.view.getSelectedRecords()[0]
			if (record){
				this.selected = record
				this.details.update_details(record.data.type, record.data.id)
			}
		}, this)
	},
	submit: function(){
		if (this.callback){
			this.callback.apply(this.scope, [this, this.selected])
		}
		this.close()
		this.fireEvent("submitted", this.selected)
	}
})
Ext.reg('vault.selectresourcedialog', Vault.SelectResourceDialog)
/**
 * @author mpeter
 */

Ext.ns("Vault")

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
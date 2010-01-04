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
			cmp = Ext.getCmp(this.parentPanel)
			dynamic = {}
			if (cmp){
				record = cmp.getSelected()
				rid = record.data.id
				config = Ext.apply(config, { rid: rid, rtype: 'resources' })
			}
			dialog = new Vault.RestfulFormDialog(config)
			dialog.show()
		}, this)
	},
})

//register xtype
Ext.reg('vault.open_form_dialog_button', Vault.OpenFormDialogButton); 

Vault.ResourceLinkField = Ext.extend(Ext.form.TextField,  {
    /**
     * @cfg {String} buttonText The button text to display on the upload button (defaults to
     * 'Browse...').  Note that if you supply a value for {@link #buttonCfg}, the buttonCfg.text
     * value will be used instead if available.
     */
    buttonText: 'Select...',
    /**
     * @cfg {Boolean} buttonOnly True to display the file upload field as a button with no visible
     * text field (defaults to false).  If true, all inherited TextField members will still be available.
     */
    buttonOnly: false,
    /**
     * @cfg {Number} buttonOffset The number of pixels of space reserved between the button and the text field
     * (defaults to 3).  Note that this only applies if {@link #buttonOnly} = false.
     */
    buttonOffset: 3,
    /**
     * @cfg {Object} buttonCfg A standard {@link Ext.Button} config object.
     */


    rtype: 'previews',

    // private
    readOnly: true,

    /**
     * @hide
     * @method autoSize
     */
    autoSize: Ext.emptyFn,

    // private
    initComponent: function(){
        Vault.ResourceLinkField.superclass.initComponent.call(this);

        this.addEvents(
            'resourceselected'
        );
    },

    // private
    onRender : function(ct, position){
        Vault.ResourceLinkField.superclass.onRender.call(this, ct, position);

        this.wrap = this.el.wrap({cls:'x-form-field-wrap x-form-file-wrap'});
        this.el.addClass('x-form-file-text');
        xpr = /(\w+)\[(\w+)\]/
        if (xpr.test(this.name)){
        	field = xpr.exec(this.name)[2]
        	class_ = xpr.exec(this.name)[1]
        	this.hidden_field_name = (class_ + '[' + field + '_id]')
        	this.text_field_name = (class_ + '[' + field + '_name]')
        } else {
        	this.hidden_field_name = + field + '_id'
        	this.text_field_name = field + '_name'
        }
        this.getEl().set({name: null})
        value = this.value
        if (value) {
			this.setValue(value.name)
		}

        var btnCfg = Ext.applyIf(this.buttonCfg || {}, {
            text: this.buttonText
        });
        this.hidden_field = new Ext.form.Hidden({
        	name : this.hidden_field_name,
        	renderTo: this.wrap
        })
        
        this.button = new Ext.Button(Ext.apply(btnCfg, {
            renderTo: this.wrap,
            cls: 'x-form-file-btn' + (btnCfg.iconCls ? ' x-btn-icon' : '')
        }));

        if(this.buttonOnly){
            this.el.hide();
            this.wrap.setWidth(this.button.getEl().getWidth());
        }

        this.bindListeners();
        this.resizeEl = this.positionEl = this.wrap;
    },
    
    bindListeners: function(){
        this.button.on({
            scope: this,
            click: function() {
                dialog = new Vault.SelectResourceDialog({
                	callback: this.select_callback,
                	scope: this,
					rtype: this.rtype,
                })
                dialog.show()
            }
        }); 
    },
    
    select_callback: function(dialog, record){
    	this.setValue(record.data.name)
    	this.hidden_field.setValue(record.data.id)
    },
    
    reset : function(){
        this.hidden_field.remove();
        this.createHiddenInputs();
        this.bindListeners();
        Vault.ResourceLinkField.superclass.reset.call(this);
    },

    // private
    getHiddenInputId: function(){
        return this.id + '-id';
    },

    // private
    onResize : function(w, h){
        Vault.ResourceLinkField.superclass.onResize.call(this, w, h);

        this.wrap.setWidth(w);

        if(!this.buttonOnly){
            var w = this.wrap.getWidth() - this.button.getEl().getWidth() - this.buttonOffset;
            this.el.setWidth(w);
        }
    },

    // private
    onDestroy: function(){
        Vault.ResourceLinkField.superclass.onDestroy.call(this);
        Ext.destroy(this.hidden_field, this.button, this.wrap);
    },
    
    onDisable: function(){
        Vault.ResourceLinkField.superclass.onDisable.call(this);
        this.doDisable(true);
    },
    
    onEnable: function(){
        Vault.ResourceLinkField.superclass.onEnable.call(this);
        this.doDisable(false);

    },
    
    // private
    doDisable: function(disabled){
        this.hidden_field.dom.disabled = disabled;
        this.button.setDisabled(disabled);
    },


    // private
    preFocus : Ext.emptyFn,

    // private
    alignErrorIcon : function(){
        this.errorIcon.alignTo(this.wrap, 'tl-tr', [2, 0]);
    }

});

Ext.reg('vault.resourcelinkfield', Vault.ResourceLinkField);


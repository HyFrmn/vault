Ext.ns('Vault')

Vault.LayoutPanel = Ext.extend(Ext.Panel, {
	// Prototype Defaults, can be overridden by user's config object
	layout: 'fit',
	
	initComponent: function(){
		// Called during component initialization

		// Config object has already been applied to 'this' so properties can 
		// be overriden here or new properties (e.g. items, tools, buttons) 
		// can be added, eg:
		Ext.apply(this, {

		});

		// Before parent code

		// Call parent (required)
		Vault.LayoutPanel.superclass.initComponent.apply(this, arguments);

		// After parent code
		// e.g. install event handlers on rendered component
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

Vault.toolbarPanel = new Ext.Panel({
	region: 'north',
	height: 32,
	layout: 'fit',
})

Vault.menuPanel = new Vault.LayoutPanel({
	region: 'west',
	id: 'west-panel',
	width: 200,
	minSize: 175,
	maxSize: 400,
	margins: '0 0 0 5',
	split: true,
})

Vault.mainPanel = new Vault.LayoutPanel({
	region: 'center',
	layout: 'fit'
}),

Vault.mainMenu = new Ext.tree.TreePanel({
    useArrows: true,
    autoScroll: true,
    animate: true,
    containerScroll: true,
    border: false,
    // auto create TreeLoader

    loader: new Ext.tree.TreeLoader({
    	dataUrl: '/application/menu',
    	baseParams: {menu: true},
    	requestMethod: 'GET',
    	listeners: {
    		load: {
    			fn: function(tl, n, r){
    				n.resource_id = n.id.split(':')[1]
    			},
    			scope: this,
    		},
    	},
    }),

    listeners: {
		beforeappend: {
			fn: function(tree, parent, node){
					node.on("click", function(){
						tmp = node.id.split(':')
						type = tmp[0]
						id = tmp[1]
						view = null
						resource_types = ['resource', 'project', 'preview']
						if ( resource_types.indexOf(type) != -1 ){
							view = Vault.newResourceDetails(id, { resultPanel: Vault.mainPanel })
						}
						if (view) {
							Vault.mainPanel.replace(view)
						}
					})
				}
		}
	},
    
    root: {
        nodeType: 'async',
        text: 'Projects',
        draggable: false,
        id: 'projects',
        listeners: {
			click: { 
					fn: function(){
							Vault.mainPanel.replace(new Vault.Grid(Vault.project_grid_config))
					},
					scope: this,
			}
		}
    }
});


Vault.viewport = function(){
	toolbar = new Ext.Toolbar();
	
	new_menu = [{
		text: "New Project",
		handler: function(){
			Vault.newProjectForm(Vault.mainPanel)
		},
	}]
	
	toolbar.add({
		text: "New",
		xtype: "button",
		menu: new_menu
	})

	Vault.toolbarPanel.add(toolbar)
	
	Vault.mainPanel.add(Vault.newResourceGrid({ project_id : 1}, { resultPanel: Vault.mainPanel }))
	Vault.menuPanel.add(Vault.mainMenu)
	
	new Ext.Viewport({
		layout: 'border',
		items: [
			Vault.toolbarPanel,
			Vault.menuPanel,
			Vault.mainPanel,
			]
	});
}
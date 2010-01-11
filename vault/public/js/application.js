// vim: sw=4:ts=4:nu:nospell:fdc=4

/*global Ext, Application */

Ext.ns('Vault');

Vault.Application = Ext.extend(Ext.Viewport,{
    layout: 'border',
    toolbar: new Ext.Toolbar({
                    region: 'north',
                    height: 32,
                    layout: 'fit',
                    }),
    statusbar: new Ext.Toolbar({
                    region: 'south',
                    height: 24,
                    layout: 'fit',
                    items: ['Nothing Selected',]
    }),
    mainPanel: new Vault.LayoutPanel({
                        region: 'center',
                        layout: 'fit'
                }),
    mainMenu: new Ext.tree.TreePanel({
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
                    }),
                    root: {
                        nodeType: 'async',
                        text: 'Projects',
                        draggable: false,
                        id: 'projects',
                    }
                }),
    menuPanel: new Vault.LayoutPanel({
                        region: 'west',
                        id: 'west-panel',
                        width: 200,
                        minSize: 175,
                        maxSize: 400,
                        margins: '0 0 0 5',
                        split: true,
                    }),
    initComponent: function(config){
        Ext.apply(this, {
        });
        Vault.Application.superclass.initComponent.apply(this, [])
        this.menuPanel.add(this.mainMenu)
        this.mainMenu.root.on("click", function(){
            this.mainPanel.replace(new Vault.Grid({ rtype: 'projects' }))
        }, this)
        this.add([
            this.toolbar,
            this.menuPanel,
            this.mainPanel,
            this.statusbar,
            ])
        this.loadToolbar()
        this.on("selectionchange", this.changeSelectionCallback, this)
        this.mainMenu.on("beforeappend", this.beforeAppendCallback, this)
    },
    loadToolbar: function(){
        Ext.Ajax.request({
            method: 'GET',
            success: function(response, options){
                items = Ext.decode(response.responseText)
                this.toolbar.add(items)
                this.toolbar.doLayout()
            },
            failure: function(response, options){
                Ext.MessageBox.show({
                    title: 'Server Error',
                    msg: 'Toolbar was not loaded.',
                    buttons: Ext.MessageBox.OK,
                    icon: Ext.MessageBox.ERROR
                })
            },
            url: '/application/toolbar',
            scope: this,
        })
    },
    changeSelectionCallback: function(record){
        this.selected = record
        //this.statusbar.removeAll(true)
        statusCmp = this.statusbar.getComponent(0)
        statusCmp.setText("Selected " + record.data.title + ' (' + record.data.type + ')')
    },
    changeProjectCallback: function(project_id){
        this.project_id = project_id
    },
    getSelected: function(){
        return this.selected
    },
    getProject: function(){
        return this.project_id
    },
    beforeAppendCallback: function(tree, parent, node){
                                node.on("click", function(){
                                    view = node.attributes.view
                                    project_id = node.attributes.project_id
                                    this.changeProjectCallback(project_id)
                                    this.mainPanel.replace(view)
                                }, this)
                            },
})

// application main entry point
Ext.onReady(function(){
	Ext.QuickTips.init();
    Vault.app = new Vault.Application()
}); 
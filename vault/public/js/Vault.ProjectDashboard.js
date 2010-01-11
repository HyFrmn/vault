/**
 * @author mpeter
 */

Ext.ns("Vault")

Vault.ProjectDashboard = Ext.extend(Vault.LayoutPanel,{
    layout: 'border',
    project_id: 1,
    title: 'Project',
    initComponent: function(arguments){
        Vault.ProjectDashboard.superclass.initComponent.apply(this, arguments)
        this.assetGrid = new Vault.AssetDataView({
            region: 'center',
            title: null,
        })
        this.detailsView = new Vault.Details()
        this.commentsGrid = new Vault.CommentGrid()
        this.versionGrid = new Vault.VersionGrid()
        this.taskGrid = new Vault.TaskGrid()
        this.tabsPanel = new Ext.TabPanel({
            region: 'south',
            height: 350,
            split: true,
            autoScroll: true,
            activeTab: 0,
            items: [this.detailsView, this.commentsGrid, this.versionGrid, this.taskGrid]
        })
        this.add(this.assetGrid, this.tabsPanel)
        this.on("selectionchange", this.changeSelectionCallback, this)
    },
    
    changeSelectionCallback: function(record){
        this.selected = record
        if (record.data.type == "assets"){
            this.detailsView.load_from_record(record)
            this.commentsGrid.store.load({
                params: {
                    resource_id: record.data.id
                    }
                })
            this.taskGrid.store.load({
                params: {
                    asset_id: record.data.id
                }
            })
        }
    }
})

Ext.reg('vault.projectdashboard', Vault.ProjectDashboard)

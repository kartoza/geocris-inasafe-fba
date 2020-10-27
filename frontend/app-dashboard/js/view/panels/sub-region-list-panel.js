define([
    'backbone',
    'underscore',
    'jquery',
    'jqueryUi',
    'js/model/overall_summary.js',
    'js/model/administrative_country_mapping.js'
], function (
    Backbone, _, $, JqueryUi,
    OverallSummaryCollection,
    AdministrativeCountryMappingCollection
) {
    return Backbone.View.extend({
        el: '#flood-sub-summary',
        sub_summary: '#flood-sub-summary',
        loading_template: '<i class="fa fa-spinner fa-spin fa-fw"></i>',
        sub_region_title_template: _.template($('#region-title-panel-template').html()),
        sub_region_item_template: _.template($('#region-summary-panel-template').html()),
        events: {
            'click .drilldown': 'drilldown'
        },
        initialize: function (opt){
            this.panel_dashboard = opt.panel_dashboard
            this.parent_region = this.panel_dashboard.parent_region
            this.parent_region_id = this.panel_dashboard.parent_region_id
            this.current_region = this.panel_dashboard.current_region
            this.collection = new OverallSummaryCollection()
            this.country_mapping_collection = null
            this.stats_data = null
            dispatcher.on(this.panel_dashboard.published_events.region_change, this.fetchRegionSummary, this)
        },
        drilldown: function(e){
            let $button = $(e.target).closest('.drilldown')
            let region = $button.attr('data-region');
            let region_id = parseInt($button.attr('data-region-id'));
            this.panel_dashboard.drilldown(region, region_id)
        },
        show_loading: function (){
            this.$el.html(this.loading_template)
        },
        fetchRegionSummary: function (){
            let that = this
            let hazard_id = this.panel_dashboard.current_hazard.id
            let sub_region_mapping = {
                district: 'sub_district',
                sub_district: null
            }
            let id_key = {
                district: 'district_id',
                sub_district: 'sub_district_id'
            }
            this.show_loading()
            this.stats_data = []
            this.parent_region = this.panel_dashboard.current_region
            this.parent_region_id = this.panel_dashboard.current_region_id
            if(this.parent_region){
                this.collection.parent_level = this.parent_region
                this.collection.parent_id = this.parent_region_id
            }
            else{
                this.collection.parent_level = null
                this.collection.parent_id = null
            }
            let sub_region = this.panel_dashboard.top_admin_level
            if(this.parent_region !== null && this.parent_region_id !== undefined){
                sub_region = sub_region_mapping[this.parent_region]
            }
            // if subregion exists, fetch data
            if(sub_region){
                this.collection.admin_level = sub_region
                this.collection.id = hazard_id
                this.country_mapping_collection =  new AdministrativeCountryMappingCollection(sub_region)
                this.collection.fetch().then((data) => {
                    if(data) {
                        that.stats_data = data
                    }
                    // fetch administrative mapping
                    let ids = data.map(item => {
                        return item[id_key[sub_region]]
                    })
                    return that.country_mapping_collection.findByIds(ids)
                }).then(()=>{
                    that.render()
                })
            }
            else {
                this.render()
            }
        },
        render: function (){
            // Render all region summary as lists
            let that = this
            let $table = $('<table></table>')
            let title_template = this.sub_region_title_template
            let item_template = this.sub_region_item_template
            let sub_region = this.collection.admin_level
            let id_field = `${sub_region}_id`
            if(this.stats_data.length > 0){
                this.stats_data.map((item, idx) => {
                    let country_mapping = that.country_mapping_collection.findWhere({
                        [id_field]: item[id_field]
                    })
                    let country_name = country_mapping?.attributes.country_name
                    $table.append(item_template({
                        region: sub_region,
                        id: item[id_field],
                        country_name: country_name,
                        name: item.name,
                        loading_template: that.loading_template,
                        impacted_road_count: item.road_stats.impacted_road_count,
                        impacted_building_count: item.building_stats.impacted_building_count,
                        impacted_population_count: item.census_population_stats.impacted_population_count,
                        trigger_status: null
                    }))
                })
                this.$el.html(title_template({
                    region: toTitleCase(sub_region.replace('_', ''))
                }));
                this.$el.append($table);
            }
            else {
                // nothing to render
                this.$el.html('')
            }
        }
    })
})

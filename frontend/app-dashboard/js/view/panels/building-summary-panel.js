define([
    'backbone',
    'jquery',
    'js/view/panels/summary-panel.js',
], function (Backbone, $, SummaryPanel, OverallSummaryCollection) {

    return SummaryPanel.extend({
        _panel_key: 'building',
        primary_exposure_key: 'residential',
        primary_exposure_label: 'Residential Buildings',
        other_category_exposure_label: 'Other Buildings',

        fetchSummary: function (){
            let that = this
            let hazard_id = this.panel_dashboard.current_hazard.id
            let current_region = this.panel_dashboard.current_region
            this.show_loading()
            this.collection.admin_level = current_region
            this.collection.id = hazard_id
            this.collection.fetch().then((data) => {
                // should only have at least one valid data
                if(data && data[0]) {
                    that.stats_data = data[0].building_stats
                }
                that.render()
            })
        }
    });
});

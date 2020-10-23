define([
    'backbone',
    'jquery',
    'js/view/panels/summary-panel.js'
], function (Backbone, $, SummaryPanel) {

    return SummaryPanel.extend({
        _panel_key: 'population',
        primary_exposure_key: 'affected',
        primary_exposure_label: 'Estimated Affected people in administrative region',
        other_category_exposure_label: 'Affected Administrative Region Demographic (based on Census Data)',

        fetchSummary: function (){
            let that = this
            let hazard_id = this.panel_dashboard.current_hazard.id
            let current_region = this.panel_dashboard.current_region
            this.collection.admin_level = current_region
            this.collection.id = hazard_id
            this.collection.fetch().then((data) => {
                that.stats_data = data.census_population_stats
                that.render()
            })
        },
        renderChartElement: function (data, exposure_name) {
            data['affected_impacted_population_count'] = data['impacted_population_count'];
            data['affected_population_count'] = data['population_count'];
            data['census_count'] = data['population_count']
            SummaryPanel.prototype.renderChartElement.call(this, data, exposure_name);
            let $parentWrapper = $(`#chart-score-panel .tab-${exposure_name}`);
            let is_exposed_census_count_exists = data['census_count'] !== undefined;
            $parentWrapper.find('.exposed-census-count').html(is_exposed_census_count_exists ? data['census_count'] : 0);
        }
    });
});

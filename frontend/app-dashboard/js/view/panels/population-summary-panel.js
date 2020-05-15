define([
    'backbone',
    'jquery',
    'js/view/panels/summary-panel.js'
], function (Backbone, $, SummaryPanel) {

    return SummaryPanel.extend({
        _panel_key: 'population',
        primary_exposure_key: 'affected',
        primary_exposure_label: 'Estimated Affected people (based on World Pop Data)',
        other_category_exposure_label: 'Affected Administrative Region Demographic (based on Census Data)',
        renderChartElement: function (data, exposure_name) {
            data['affected_hazarded_population_count'] = data['hazarded_population_count'];
            data['affected_population_count'] = data['population_count'];
            SummaryPanel.prototype.renderChartElement.call(this, data, exposure_name);
            let $parentWrapper = $(`#chart-score-panel .tab-${exposure_name}`);
            let is_exposed_census_count_exists = data['census_count'] !== undefined;
            $parentWrapper.find('.exposed-census-count').html(is_exposed_census_count_exists ? data['census_count'] : 0);
        }
    });
});

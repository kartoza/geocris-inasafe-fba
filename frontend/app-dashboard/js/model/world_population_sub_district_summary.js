define([
    'backbone',
    'moment'
], function (Backbone) {

    const WorldPopulationSubDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_flood_event_population_sub_district_summary',
        url: function () {
            return `${this.urlRoot}?flood_event_id=eq.${this.get('flood_event_id')}&sub_district_id=eq.${this.get('sub_district_id')}`
        }
    });

    return Backbone.Collection.extend({
        model: WorldPopulationSubDistrictSummary,
        urlRoot: postgresUrl + 'mv_flood_event_population_sub_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

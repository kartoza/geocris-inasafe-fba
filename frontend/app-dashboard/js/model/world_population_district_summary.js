define([
    'backbone',
    'moment'
], function (Backbone) {

    const WorldPopulationDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_flood_event_population_district_summary',
        url: function () {
            return `${this.urlRoot}?flood_event_id=eq.${this.get('flood_event_id')}&district_id=eq.${this.get('district_id')}`
        }
    });

    return Backbone.Collection.extend({
        model: WorldPopulationDistrictSummary,
        urlRoot: postgresUrl + 'mv_flood_event_population_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

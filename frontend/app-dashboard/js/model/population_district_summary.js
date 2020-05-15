define([
    'backbone',
    'moment'
], function (Backbone) {

    const PopulationDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_population_district_summary',
        url: function () {
            return `${this.urlRoot}?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: PopulationDistrictSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_population_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

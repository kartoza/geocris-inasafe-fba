define([
    'backbone',
    'moment'
], function (Backbone) {

    const PopulationSubDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_population_sub_district_summary',
        url: function () {
            return `${this.urlRoot}?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: PopulationSubDistrictSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_population_sub_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

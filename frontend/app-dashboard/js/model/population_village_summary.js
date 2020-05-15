define([
    'backbone',
    'moment'
], function (Backbone) {

    const PopulationVillageSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_population_village_summary',
        url: function () {
            return `${this.urlRoot}?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: PopulationVillageSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_population_village_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

define([
    'backbone',
    'moment'
], function (Backbone) {

    const WorldPopulationVillageSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_flood_event_population_village_summary',
        url: function () {
            return `${this.urlRoot}?flood_event_id=eq.${this.get('flood_event_id')}&village_id=eq.${this.get('village_id')}`
        }
    });

    return Backbone.Collection.extend({
        model: WorldPopulationVillageSummary,
        urlRoot: postgresUrl + 'mv_flood_event_population_village_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

define([
    'backbone',
    'moment'
], function (Backbone) {

    const WorldPopulationVillageSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_world_pop_village_summary',
        url: function () {
            return `${this.urlRoot}?hazard_event_id=eq.${this.get('hazard_event_id')}&village_id=eq.${this.get('village_id')}`
        }
    });

    return Backbone.Collection.extend({
        model: WorldPopulationVillageSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_world_pop_village_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

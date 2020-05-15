define([
    'backbone',
    'moment'
], function (Backbone) {

    const WorldPopulationDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_world_pop_district_summary',
        url: function () {
            return `${this.urlRoot}?hazard_event_id=eq.${this.get('hazard_event_id')}&district_id=eq.${this.get('district_id')}`
        }
    });

    return Backbone.Collection.extend({
        model: WorldPopulationDistrictSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_world_pop_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

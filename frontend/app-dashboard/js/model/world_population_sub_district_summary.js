define([
    'backbone',
    'moment'
], function (Backbone) {

    const WorldPopulationSubDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_world_pop_sub_district_summary',
        url: function () {
            return `${this.urlRoot}?hazard_event_id=eq.${this.get('hazard_event_id')}&sub_district_id=eq.${this.get('sub_district_id')}`
        }
    });

    return Backbone.Collection.extend({
        model: WorldPopulationSubDistrictSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_world_pop_sub_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

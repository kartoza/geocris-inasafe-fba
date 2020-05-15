define([
    'backbone',
    'moment'
], function (Backbone) {

    const RoadVillageSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_road_village_summary',
        url: function () {
            return `${this.urlRoot}?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: RoadVillageSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_road_village_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

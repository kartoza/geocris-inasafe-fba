define([
    'backbone',
    'moment'
], function (Backbone) {

    const RoadDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_road_district_summary',
        url: function () {
            return `${this.urlRoot}?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: RoadDistrictSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_road_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

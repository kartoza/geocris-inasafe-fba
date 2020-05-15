define([
    'backbone',
    'moment'
], function (Backbone) {

    const RoadSubDistrictSummary = Backbone.Model.extend({
        urlRoot: postgresUrl + 'mv_hazard_event_road_sub_district_summary',
        url: function () {
            return `${this.urlRoot}?id=eq.${this.id}`
        }
    });

    return Backbone.Collection.extend({
        model: RoadSubDistrictSummary,
        urlRoot: postgresUrl + 'mv_hazard_event_road_sub_district_summary',
        url: function () {
            return this.urlRoot;
        }
    });
});

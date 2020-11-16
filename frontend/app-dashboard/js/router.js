define(['backbone'], function (Backbone) {

    return Backbone.Router.extend({
        parameters: {},
        routes: {
            "": "landingPage",
            "hazard/:hazardId": "hazardEventSummary",
            "hazard/:hazardId/:country/:countryId": "hazardDrillDownSummary",
            "hazard/:hazardId/:country/:countryId/:district/:districtId": "hazardDrillDownSummary",
            "hazard/:hazardId/:country/:countryId/:district/:districtId/:subDistrict/:subDistrictId": "hazardDrillDownSummary",
        },
        landingPage: function () {
            console.log('landing page');
        },
        _callPromise: function (event, ...params) {
            return new Promise(function (resolve, reject) {
                setTimeout(function () {
                    dispatcher.trigger(event, ...params);
                    resolve('')
                }, 500)
            })
        },
        hazardEventSummary: function (hazardId) {
            this._callPromise('hazard:fetch-hazard-event-summary', hazardId)
        },
        _drillDown: function (...drillDownParams) {
            const that = this;
            that._callPromise('dashboard:drilldown', drillDownParams[0], drillDownParams[1]).then(function () {
                drillDownParams.splice(0, 2)
                if (drillDownParams.length >= 2) {
                    that._drillDown(...drillDownParams)
                }
            });
        },
        hazardDrillDownSummary: function (hazardId, ...drillDownParams) {
            const that = this;
            drillDownParams = drillDownParams.filter(function (el) {
                return el != null;
            });
            this._callPromise('hazard:fetch-hazard-event-summary', hazardId).then(function () {
                that._drillDown(...drillDownParams);
            })
        },
    })

});
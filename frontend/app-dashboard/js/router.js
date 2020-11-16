define(['backbone'], function (Backbone) {

    return Backbone.Router.extend({
        parameters: {},
        routes: {
            "": "landingPage",
            "hazard/:hazardId": "hazardEventSummary",
            "hazard/:hazardId/:country/:countryId": "hazardCountrySummary",
            "hazard/:hazardId/:country/:countryId/:district/:districtId": "hazardDistrictSummary",
            "hazard/:hazardId/:country/:countryId/:district/:districtId/:subDistrict/:subDistrictId": "hazardSubDistrictSummary",
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
        hazardCountrySummary: function (hazardId, country, countryId) {
            let that = this;
            this._callPromise('hazard:fetch-hazard-event-summary', hazardId).then(function () {
                that._callPromise('dashboard:drilldown', country, countryId);
            })
        },
        hazardDistrictSummary: function (hazardId, country, countryId, district, districtId) {
            let that = this;
            this._callPromise('hazard:fetch-hazard-event-summary', hazardId).then(function () {
                that._callPromise('dashboard:drilldown', country, countryId).then(function () {
                    that._callPromise('dashboard:drilldown', district, districtId)
                });
            })
        },
        hazardSubDistrictSummary: function (hazardId, country, countryId, district, districtId, subDistrict, subDistrictId) {
            let that = this;
            this._callPromise('hazard:fetch-hazard-event-summary', hazardId).then(function () {
                that._callPromise('dashboard:drilldown', country, countryId).then(function () {
                    that._callPromise('dashboard:drilldown', district, districtId).then(function () {
                        that._callPromise('dashboard:drilldown', subDistrict, subDistrictId)
                    })
                });
            })
        }
    })

});
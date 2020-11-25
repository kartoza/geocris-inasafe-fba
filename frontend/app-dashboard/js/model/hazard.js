define([
    'backbone',
    'leaflet'
], function (Backbone, L) {

    const Hazard = Backbone.Model.extend({
        urlRoot: fbaProxyURL + '/api/hazard-event/',
        id: null,
        extent: null,
        _constants: {
            PRE_ACTIVATION_TRIGGER: 1,
            ACTIVATION_TRIGGER: 2,
            WMS_LAYER_NAME: function (hazard_type) {
                return `${layerNamespace}${hazard_type}_forecast_layer`
            }
        },
        url: function () {
            return `${this.urlRoot}/${this.id}/`;
        },
        fetchExtent: function () {
            const that = this;
            return new Promise(function (resolve, reject) {
                $.ajax({
                    url: `${that.urlRoot}/${that.id}/extent`,
                    success: function (data) {
                        if (typeof data === 'object' && data !== null) {
                            if (Object.keys(data).length > 0) {
                                that.extent = {
                                    x_min: data.x_min,
                                    x_max: data.x_max,
                                    y_min: data.y_min,
                                    y_max: data.y_max,
                                    leaflet_bounds: [
                                        [data.y_min, data.x_min],
                                        [data.y_max, data.x_max]
                                    ]
                                }
                                resolve(that.extent)
                            }
                        }
                        reject('Data error');
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        reject(XMLHttpRequest.responseText)
                    }
                });
            })
        },
        fetchSummary: function () {
            const that = this;
            return new Promise(function (resolve, reject) {
                $.ajax({
                    url: `${that.urlRoot}/${that.id}/summary-stats/district`,
                    success: function (data) {
                        if (data.length > 0) {
                            resolve(data)
                        }
                        reject('Empty');
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        reject(XMLHttpRequest.responseText)
                    }
                });
            })
        },
        leafletLayer: function () {
            return L.tileLayer.wms(
                geoserverUrl,
                {
                    layers: this._constants.WMS_LAYER_NAME(this.hazardTypeSlug()),
                    format: 'image/png',
                    transparent: true,
                    srs: 'EPSG:4326',
                    tiled: true,
                    filter: toXmlAndFilter({id: this.get('id')})
                });
        },
        hazardTypeSlug: function () {
            return this.get('hazard_type').toLowerCase().replace(' ', '_');
        }
    });

    return Backbone.Collection.extend({
        model: Hazard,
        urlRoot: fbaProxyURL + '/api/hazard-event/recent/',
        url: function () {
            return this.urlRoot;
        }
    });

});


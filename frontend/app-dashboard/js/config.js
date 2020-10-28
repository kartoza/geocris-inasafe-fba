require.config({
    baseUrl: 'js/',
    paths: {
        'jquery': 'libs/jquery.js/3.4.1/jquery.min',
        'jqueryUi': 'libs/jquery-ui-1.12.1/jquery-ui.min',
        'backbone': 'libs/backbone.js/1.4.0/backbone-min',
        'leaflet': 'libs/leaflet/1.5.1/leaflet-src',
        'bootstrap': 'libs/bootstrap-4.4.1/js/bootstrap.bundle.min',
        'underscore': 'libs/underscore.js/1.9.1/underscore-min',
        'moment': 'libs/moment/2.24.0/moment.min',
        'rangeSlider': 'libs/ion-rangeslider/2.3.0/js/ion.rangeSlider.min',
        'leafletDraw': 'libs/leaflet.draw/1.0.4/leaflet.draw',
        'wellknown': 'libs/wellknown.js/0.5.0/wellknown',
        'airDatepicker': 'libs/airdatepicker/js/datepicker',
        'airDatepickerEN': 'libs/airdatepicker/js/i18n/datepicker.en',
        'chartjs': 'libs/chart/Chart-2.7.2',
        'chartPluginLabel': 'libs/chart-plugin-label/chartjs-plugin-labels',
        'markdown': 'libs/markdown-it-10.0.0/markdown-it.min',
        'filesaver': 'libs/filesaver/FileSaver',
        'leafletWMSLegend': 'libs/leaflet-wms-legend/leaflet.wmslegend',
        'leafletAwesomeIcon': 'libs/leaflet.awesome-markers/js/leaflet.awesome-markers'
    },
    shim: {
        moment: {
            exports: 'moment'
        },
        leaflet: {
            exports: 'L'
        },
        bootstrap: {
            deps: ["jquery"]
        },
        rangeSlider: {
            deps: ["jquery"]
        },
        leafletDraw: {
            deps: ['leaflet'],
            exports: 'LeafletDraw'
        },
        airDatepicker: {
            deps: ['jquery', 'jqueryUi', 'bootstrap']
        },
        airDatepickerEN: {
            deps: ['jquery', 'jqueryUi', 'bootstrap', 'airDatepicker']
        },
        utils: {
            deps: ['moment'],
            exports: 'utils'
        },
        filesaver: {
            deps: ["jquery"]
        },
        leafletWMSLegend: {
            deps: ['leaflet']
        },
        leafletAwesomeIcon: {
            deps: ['leaflet']
        },
        chartPluginLabel: {
            deps: ['chartjs']
        }
    }
});
require([
    'jquery',
    'bootstrap',
    'backbone',
    'underscore',
    'moment',
    'leaflet',
    'leafletDraw',
    'airDatepicker',
    'airDatepickerEN',
    'utils',
    'js/view/map.js',
    'js/request.js',
    'js/view/summary-collection.js',
    'js/model/hazard_type.js',
], function ($, bootstrap, Backbone, _, moment, L, LDraw, AirDatepicker, AirDatepickerEN, utils, Map, RequestView, FloodCollectionView, HazardTypeCollection) {
    AppRequest = new RequestView();
    dispatcher = _.extend({}, Backbone.Events);

    // Initialize all tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // we get the hazardTypeCollection
    hazardTypeCollection = new HazardTypeCollection()
    hazardTypeCollection.fetch().then(function (data) {
        mapView = new Map();
        floodCollectionView = new FloodCollectionView();
    }).catch(function (data) {
        console.log('Hazard type request failed');
        console.log(data);
    });
});

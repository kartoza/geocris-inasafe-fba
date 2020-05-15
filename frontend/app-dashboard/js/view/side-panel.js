define([
    'backbone',
    'underscore',
    'jquery',
    'jqueryUi',
    'js/view/layers/upload-hazard.js',
    'js/view/panel-dashboard.js',
], function (Backbone, _, $, JqueryUi, HazardUploadView, DashboardView) {
    return Backbone.View.extend({
        el: "#side-panel",
        events: {
            'click .add-hazard-scenario': 'openPanelHazardScenario',
            'click .btn-back': 'backButtonAction',
            'click #upload-hazard': 'openUploadHazardForm',
            'click .browse-hazards': 'openBrowseHazard',
            'click .hide-browse-hazard': 'hideBrowseHazard',
            'click .browse-arrow': 'fetchHazardById',
            'click #btn-browse-forecast': 'openBrowseByForecast',
            'click #btn-browse-return-period': 'openBrowseByReturnPeriod'
        },
        initialize: function () {
            let that = this;
            this.dashboard = new DashboardView();
            $('.add-hazard-scenario').click(function () {
                that.openPanelHazardScenario()
            });

            $('.browse-hazards').click(function () {
                dispatcher.trigger('intro:hide');
                that.openBrowseHazard()
            });

            // Initialize view
            this.hazard_upload_view = new HazardUploadView();
            dispatcher.on('side-panel:open-dashboard', this.openDashboard, this);
            dispatcher.on('side-panel:open-welcome', this.openWelcome, this);
        },
        openPanelHazardScenario: function () {
            resetView = false;
            dispatcher.trigger('dashboard:hide');
            $('.panel-body-wrapper').not('.panel-hazard-scenario').not('.floating-panel').hide();
            $('.panel-hazard-scenario').show("slide", { direction: "right" }, 400);
        },
        backButtonAction: function (e) {
            $('form').trigger('reset');
            $('.default-disabled').prop('disabled', true);
            $(e.target).closest('.panel-body-subwrapper').hide();
            let $wrapper = $(e.target).closest('.panel-body-wrapper');
            $wrapper.hide("slide", { direction: "right" }, 300);
            $wrapper.prev().show("slide", { direction: "right" }, 400);
        },
        openUploadHazardForm: function (e) {
            $('.panel-body-wrapper').not('.panel-hazard-form').not('.floating-panel').hide();
            let $wrapper = $('.panel-hazard-form');
            $wrapper.show();
            $wrapper.find('.panel-upload-hazard').show("slide", { direction: "right" }, 500);
        },
        removeIntroWindow: function (e) {
            // Hide the intro window
            dispatcher.trigger('intro:hide');
        },
        openBrowseHazard: function (e) {
            $('.browse-btn-icon').hide();
            $('.panel-browse-hazard').show("slide", { direction: "down" }, 400);
            $('.arrow-start').hide();
            $('.browse-hazards').removeClass('bounce-7');
        },
        hideBrowseHazard: function () {
            $('.browse-btn-icon').show();
            $('.panel-browse-hazard').hide("slide", { direction: "down" }, 400);
        },
        fetchHazardById: function (e) {
            let hazard_id = $(e.target).closest('.browse-arrow').attr('data-hazard-id');
            dispatcher.trigger('hazard:fetch-hazard-by-id', hazard_id);
        },
        openBrowseByForecast: function (e) {
            $(e.target).closest('.panel-body-wrapper').hide();
            let $wrapper = $('.panel-browse-by-forecast');
            $wrapper.show();
            $wrapper.parent().show("slide", { direction: "right" }, 400);
        },
        openBrowseByReturnPeriod: function (e) {
            $(e.target).closest('.panel-body-wrapper').hide();
            let $wrapper = $('.panel-browse-by-return-period');
            $wrapper.show();
            $wrapper.parent().show("slide", { direction: "right" }, 400);
        },
        openDashboard: function (callback) {
            this.dashboard.render(callback);
            $('.panel-body-wrapper').not('.floating-panel').hide();
            $('#panel-dashboard').show("slide", { direction: "right" }, 400);
        },
        openWelcome: function () {
            $('#panel-dashboard').hide();
            this.hideBrowseHazard();
            $('.panel-body-wrapper').not('.panel-welcome').not('.floating-panel').hide();
            $('.panel-welcome').show("slide", { direction: "right" }, 400);
            $('.browse-hazards').addClass('bounce-7');
        }
    })
});

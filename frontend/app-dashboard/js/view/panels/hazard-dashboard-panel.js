define([
    'backbone',
    'jquery',
    'utils',
    'js/view/panels/building-summary-panel.js',
    'js/view/panels/road-summary-panel.js',
    'js/view/panels/population-summary-panel.js',
], function (Backbone, $, utils,
             BuildingSummaryPanel,
             RoadSummaryPanel,
             PopulationSummaryPanel
             ) {

    return Backbone.View.extend({
        template: _.template($('#dashboard-template').html()),
        loading_template: '<i class="fa fa-spinner fa-spin fa-fw"></i>',
        general_summary: '#flood-general-summary',
        el: '#panel-dashboard',
        events: {
            'click .drilldown': 'drilldown',
            'click .btn-back-summary-panel': 'backPanelDrilldown',
            'click .download-spreadsheet': 'fetchExcel',
            'click .tab-title': 'switchTab'
        },
        initialize: function () {
            this.summary_collection = floodCollectionView
            this.current_region = 'district'
            this.current_region_id = null
            this.current_hazard = null

            // summary panels
            this.summary_panels = {
                'building': new BuildingSummaryPanel(this),
                'road': new RoadSummaryPanel(this),
                'population': new PopulationSummaryPanel(this)
            }
            // events
            dispatcher.on('dashboard:reset', this.resetDashboard, this);
            dispatcher.on('dashboard:hide', this.hideDashboard, this);
        },
        selectHazard: function (hazard) {
            // load hazard data
            this.current_hazard = hazard
            this.render()
        },
        resetDashboard: function () {
            this.referer_region = [];
            this.panel_handlers.map(o => o.stats_data = []);
            $(this.status_wrapper).html('-');
            $(this.general_summary).empty().html('' +
                '<div class="panel-title">' +
                '        No data available.' +
                '    </div>');
            $('#status').removeClass().addClass('trigger-status-none');
        },
        hideDashboard: function () {
            this.referer_region = [];
            let $datepicker = $('.datepicker-browse');
            let datepicker_data = $datepicker.data('datepicker');
            datepicker_data.clear();
            $('#panel-dashboard').hide();
        },
        render: function (){
            // render main information panel
            this.referer_region = [];
            let that = this;
            let $action = $(that.status_wrapper);
            $action.html(that.loading_template);
            let flood_acquisition_date = new Date(floodCollectionView.selected_forecast.attributes.acquisition_date);
            let flood_forecast_date = new Date(floodCollectionView.selected_forecast.attributes.forecast_date);

            let lead_time = floodCollectionView.selected_forecast.attributes.lead_time;
            if (typeof lead_time === 'undefined') {
                lead_time = '-';
            }
            let event_status = 'Current';
            if(floodCollectionView.selected_forecast.attributes.is_historical){
                event_status = 'Historical'
            }
            let attrs = this.current_hazard.attributes
            this.$el.find(this.general_summary).html(
                this.template({
                    hazard_type: attrs.hazard_type,
                    name: attrs.hazard_map.place_name,
                    acquisition_date: flood_acquisition_date.getDate() + ' ' + monthNames[flood_acquisition_date.getMonth()] + ' ' + flood_acquisition_date.getFullYear(),
                    forecast_date: flood_forecast_date.getDate() + ' ' + monthNames[flood_forecast_date.getMonth()] + ' ' + flood_forecast_date.getFullYear(),
                    source: attrs.source,
                    notes: attrs.notes,
                    link: attrs.link,
                    lead_time: lead_time + ' Day(s)',
                    event_status: event_status
                })
            )
            // render charts
        }
    })
})

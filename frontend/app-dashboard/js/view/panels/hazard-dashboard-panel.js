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
        status_wrapper: '#action-status',
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

            // Show back button
            $('.btn-back-summary-panel').show();

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

            // Panel header
            $action.html(`Summary for ${attrs.hazard_map.place_name}`);

            // render charts
        },
        backPanelDrilldown: function (e) {
            let that = this;
            this.referer_region.pop();

            let $button = $(e.target).closest('.btn-back-summary-panel');
            let region = $button.attr('data-region');
            let region_id = $button.attr('data-region-id');
            let trigger_status = $button.attr('data-region-trigger-status');
            let main = false;
            if(region_id === ''){
                dispatcher.trigger('flood:deselect-forecast')
                return
            }
            if(region_id === 'main'){
                main = true
            }

            let referer_region = '';
            let referer_region_id = '';
            let referer_trigger_status = 0;
            try {
                this.referer_region.pop();
                referer_region = that.referer_region[that.referer_region.length - 1].region;
                referer_region_id = that.referer_region[that.referer_region.length - 1].id;
                referer_trigger_status = that.referer_region[that.referer_region.length - 1].trigger_status;
            }catch (err){

            }

            $('.btn-back-summary-panel')
                .attr('data-region', referer_region)
                .attr('data-region-id', referer_region_id)
                .attr('data-region-trigger-status', referer_trigger_status);
            this.changeStatus(trigger_status);
            this.panel_handlers.map(o => o.stats_data = []);
            dispatcher.trigger('flood:fetch-stats-data', region, region_id, main, 'building');
            dispatcher.trigger('flood:fetch-stats-data', region, region_id, main, 'road');
            dispatcher.trigger('flood:fetch-stats-data', region, region_id, main, 'population');
            this.fetchExtent(region_id, region);
            let forecast_id = floodCollectionView.selected_forecast.id;
            let hazard_type_slug = floodCollectionView.selected_forecast.hazardTypeSlug();
            dispatcher.trigger('map:show-exposed-roads', forecast_id, hazard_type_slug, region, region_id);
            dispatcher.trigger('map:show-region-boundary', region, region_id);
            dispatcher.trigger('map:show-exposed-buildings', forecast_id, hazard_type_slug, region, region_id);
        },
    })
})

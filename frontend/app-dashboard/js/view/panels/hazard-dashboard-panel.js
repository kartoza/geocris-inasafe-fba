define([
    'backbone',
    'jquery',
    'utils',
    'js/view/panels/building-summary-panel.js',
    'js/view/panels/road-summary-panel.js',
    'js/view/panels/population-summary-panel.js',
    'js/view/panels/sub-region-list-panel.js'
], function (Backbone, $, utils,
             BuildingSummaryPanel,
             RoadSummaryPanel,
             PopulationSummaryPanel,
             SubRegionListPanel
             ) {

    return Backbone.View.extend({
        template: _.template($('#dashboard-template').html()),
        loading_template: '<i class="fa fa-spinner fa-spin fa-fw"></i>',
        general_summary: '#flood-general-summary',
        status_wrapper: '#action-status',
        back_button: '.btn-back-summary-panel',
        chart_score_panel: '#chart-score-panel',
        top_admin_level: 'district',
        el: '#panel-dashboard',
        events: {
            'click .btn-back-summary-panel': 'backPanelDrilldown',
            'click .download-spreadsheet': 'fetchExcel',
            'click .tab-title': 'switchTab'
        },
        // for convention, we declare which events fired by this view class
        published_events: {
            region_change: 'hazard-dashboard:region-change',
            hide: 'hazard-dashbord:hide',
            reset: 'hazard-dashboard:reset',
            open: 'hazard-dashboard:open',
            hazard_selected: 'hazard-dashboard:hazard-selected'
        },
        initialize: function () {
            this.referer_region = [];
            this.summary_collection = floodCollectionView
            this.parent_region = null
            this.parent_region_id = null
            this.current_region = null
            this.current_region_id = null
            this.current_hazard = null
            this.$back_button = this.$el.find(this.back_button)
            this.$chart_score_panel = this.$el.find(this.chart_score_panel)

            instance_options = {
                panel_dashboard: this
            }
            // summary panels
            this.summary_panels = {
                'building': new BuildingSummaryPanel(instance_options),
                'road': new RoadSummaryPanel(instance_options),
                'population': new PopulationSummaryPanel(instance_options)
            }

            // Subregion panel
            this.sub_region_panel = new SubRegionListPanel(instance_options)
            // events
            dispatcher.on('dashboard:reset', this.resetDashboard, this);
            dispatcher.on('dashboard:hide', this.hideDashboard, this);
        },
        selectHazard: function (hazard) {
            // load hazard data
            this.current_hazard = hazard
            this.render()
            dispatcher.trigger(this.published_events.hazard_selected)
            dispatcher.trigger(this.published_events.region_change)
        },
        resetDashboard: function () {
            this.referer_region = [];
            this.parent_region = null
            this.parent_region_id = null
            this.current_region = null
            this.current_region_id = null
            this.current_hazard = null
            $(this.status_wrapper).html('-');
            $(this.general_summary).empty().html('' +
                '<div class="panel-title">' +
                '        No data available.' +
                '    </div>');
            $('#status').removeClass().addClass('trigger-status-none');
            dispatcher.trigger(this.published_events.reset)
        },
        hideDashboard: function () {
            this.referer_region = [];
            this.parent_region = null
            this.parent_region_id = null
            this.current_region = null
            this.current_region_id = null
            this.current_hazard = null
            let $datepicker = $('.datepicker-browse');
            let datepicker_data = $datepicker.data('datepicker');
            datepicker_data.clear();
            $('#panel-dashboard').hide();
            dispatcher.trigger(this.published_events.hide)
        },
        switchTab: function (e) {
            let $div = $(e.target).closest('.tab-title');
            if(!$div.hasClass('tab-active')) {
                this.$el.find('.tab-wrapper').hide();
                this.$el.find('.tab-title').removeClass('tab-active').removeClass('col-lg-6');
                this.$el.find('.tab-title').each(function () {
                    let that = this;
                    if(!$(that).hasClass('col-lg-3')){
                        $(that).addClass('col-lg-3')
                    }
                });
                $div.addClass('tab-active').removeClass('col-lg-3').addClass('col-lg-6');
                $('.tab-name').hide();
                $div.find('.tab-name').show();
                let target = $div.attr('tab-target');
                $('.tab-' + target).show();
            }
        },
        fetchExcel: function (){
            let that = this;
            const modal = $('#fbf-modal');
            let $loadingIcon = this.$el.find('.download-spreadsheet-loading');
            $loadingIcon.show();
            $loadingIcon.closest('button').prop('disabled', true);
            $.post({
                url: `${postgresUrl}rpc/flood_event_spreadsheet`,
                data: {
                    "hazard_event_id":floodCollectionView.selected_forecast.attributes.id
                },
                success: function (data) {
                    $loadingIcon.hide();
                    $loadingIcon.closest('button').prop('disabled', false);
                    if (data.length > 0 && data[0].hasOwnProperty('spreadsheet_content') && data[0]['spreadsheet_content']) {
                        that.downloadSpreadsheet(data[0]['spreadsheet_content']);
                    } else {
                        modal.find('.modal-body-content').html('Summary data could not be found.');
                        modal.modal(
                            'toggle'
                        );
                    }
                },
                error: function () {
                    $loadingIcon.hide();
                    $loadingIcon.closest('button').prop('disabled', false);
                }
            })
        },
        fetchExtent: function (region, region_id) {
            if(!region_id || !region){
                return []
            }

            if(region_id === undefined){
                dispatcher.trigger('map:fit-forecast-layer-bounds', this.current_hazard)
            }

            if(region_id !== undefined) {
                $.get({
                    url: postgresUrl + `vw_${region}_extent?id_code=eq.${region_id}`,
                    success: function (data) {
                        if (data.length > 0) {
                            let coordinates = [[data[0].y_min, data[0].x_min], [data[0].y_max, data[0].x_max]];
                            dispatcher.trigger('map:fit-bounds', coordinates)
                        }
                    }
                });
            }
        },
        drilldown: function (new_admin_level, new_admin_id){
            // push new state to the breadcrumb stack
            this.referer_region.push({
                region: new_admin_level,
                id: new_admin_id
            })
            // use current state as parent admin boundary
            this.parent_region = this.current_region
            this.parent_region_id = this.current_region_id
            // use the new state
            this.current_region = new_admin_level
            this.current_region_id = new_admin_id
            // trigger re-render
            this.render()
            // trigger view change
            dispatcher.trigger(this.published_events.region_change)
            // trigger map change
            this.fetchExtent(new_admin_level, new_admin_id)
        },
        backPanelDrilldown: function () {
            // remove current region state level
            let referer_empty = false
            if(this.referer_region.length == 0){
                referer_empty = true
            }
            this.referer_region.pop();

            // we can get parent information either from the referer_region stack
            // or via button data attribute
            let $button = this.$back_button
            let region = $button.attr('data-region');
            let region_id = $button.attr('data-region-id');
            // no parent means return to hazard selections
            if(referer_empty){
                this.resetDashboard()
                dispatcher.trigger('flood:deselect-forecast')
                return
            }
            // We have parent id, so return to the parent admin level view
            // Update, admin level information
            try{
                let current_region = this.referer_region[this.referer_region.length - 1]
                this.current_region = current_region.region
                this.current_region_id =  current_region.id
            }
            catch(err){
                // set to null if not possible
                this.current_region = null
                this.current_region_id = null
            }

            // If we have parent information, update that as well
            try{
                let parent_region = this.referer_region[this.referer_region.length - 2]
                this.parent_region = parent_region.region
                this.parent_region_id = parent_region.id
            }
            catch(err){
                this.parent_region = null
                this.parent_region_id = null
            }

            // trigger rerender
            this.render()
            dispatcher.trigger(this.published_events.region_change)
            // trigger map change
            this.fetchExtent(new_admin_level, new_admin_id)
        },
        render: function (){
            // TODO: should also render JS route in the browser navbar URL

            // render main information panel
            let that = this;
            let $action = $(that.status_wrapper);
            $action.html(that.loading_template);

            // Show back button
            this.$back_button = this.$el.find(this.back_button)
            this.$back_button.show();
            // embed back button information
            this.$back_button
                .attr('data-region', this.parent_region)
                .attr('data-region-id', this.parent_region_id)

            let acquisition_date = new Date(this.current_hazard.attributes.acquisition_date);
            let forecast_date = new Date(this.current_hazard.attributes.forecast_date);

            let lead_time = this.current_hazard.attributes.lead_time;
            if (typeof lead_time === 'undefined') {
                lead_time = '-';
            }
            let event_status = 'Current';
            if(this.current_hazard.attributes.is_historical){
                event_status = 'Historical'
            }
            let attrs = this.current_hazard.attributes
            this.$el.find(this.general_summary).html(
                this.template({
                    hazard_type: attrs.hazard_type,
                    name: attrs.hazard_map.place_name,
                    acquisition_date: acquisition_date.getDate() + ' ' + monthNames[acquisition_date.getMonth()] + ' ' + acquisition_date.getFullYear(),
                    forecast_date: forecast_date.getDate() + ' ' + monthNames[forecast_date.getMonth()] + ' ' + forecast_date.getFullYear(),
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
            this.$chart_score_panel = this.$el.find(this.chart_score_panel)
            // If we don't have any region selected, then don't display summaries
            if(this.current_region_id !== null && this.current_region_id !== undefined) {
                this.$chart_score_panel.show()
            }
            else{
                this.$chart_score_panel.hide()
            }
            // render map
            dispatcher.trigger('map:show-exposed-roads', this.current_hazard.id, this.current_hazard.hazardTypeSlug(), this.current_region, this.current_region_id);
            dispatcher.trigger('map:show-region-boundary', this.current_region, this.current_region_id);
            dispatcher.trigger('map:show-exposed-buildings', this.current_hazard.id, this.current_hazard.hazardTypeSlug(), this.current_region, this.current_region_id);
        }
    })
})

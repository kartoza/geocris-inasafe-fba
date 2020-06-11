define([
    'backbone',
    'underscore',
    'jquery',
    'jqueryUi',
    'chartjs',
    'chartPluginLabel',
    'filesaver',
    'js/model/trigger_status.js',
    'js/view/panels/building-summary-panel.js',
    'js/view/panels/road-summary-panel.js',
    'js/view/panels/population-summary-panel.js',
], function (Backbone, _, $, JqueryUi, Chart, ChartJsPlugin, fileSaver, TriggerStatusCollection,
            BuildingSummaryPanel,
            RoadSummaryPanel,
            PopulationSummaryPanel
) {
    return Backbone.View.extend({
        template: _.template($('#dashboard-template').html()),
        loading_template: '<i class="fa fa-spinner fa-spin fa-fw"></i>',
        status_wrapper: '#action-status',
        general_summary: '#flood-general-summary',
        sub_summary: '#flood-sub-summary',
        el: '#panel-dashboard',
        referer_region: [],
        sub_region_title_template: _.template($('#region-title-panel-template').html()),
        sub_region_item_template: _.template($('#region-summary-panel-template').html()),
        status_text: {
            [TriggerStatusCollection.constants.ACTIVATION]: 'REACHED - Activate your EAP',
            [TriggerStatusCollection.constants.PRE_ACTIVATION]: 'Stand by',
            [TriggerStatusCollection.constants.NOT_ACTIVATED]: 'No Activation'
        },
        events: {
            'click .drilldown': 'drilldown',
            'click .btn-back-summary-panel': 'backPanelDrilldown',
            'click .download-spreadsheet': 'fetchExcel',
            'click .tab-title': 'switchTab'
        },
        initialize: function () {

            panel_handlers = [
                new BuildingSummaryPanel(this),
                new RoadSummaryPanel(this),
                new PopulationSummaryPanel(this)
            ]
            this.panel_handlers = panel_handlers
            this.panel_handlers_hash = {}
            this.panel_handlers.map(o => this.panel_handlers_hash[o.panelKey()] = o)

            panel_handlers.map(p => {
               let key = p.panelKey();
               dispatcher.on(`dashboard:render-chart-${key}`, p.renderChartElement, p);
            });

            this.referer_region = [];
            dispatcher.on('dashboard:reset', this.resetDashboard, this);
            dispatcher.on('dashboard:hide', this.hideDashboard, this);
            dispatcher.on('dashboard:render-region-summary', this.renderRegionSummary, this);
            dispatcher.on('dashboard:inject-exposed-region-summary', this.injectExposedRegionSummary, this);
            dispatcher.on('dashboard:change-trigger-status', this.changeStatus, this);

            this.$el = $(this.el);
        },
        render: function (callback) {
            this.referer_region = [];
            let that = this;
            let $action = $(that.status_wrapper);
            $action.html(that.loading_template);

            let general_template = that.template;

            let flood_acquisition_date = new Date(floodCollectionView.selected_forecast.attributes.acquisition_date);
            let flood_forecast_date = new Date(floodCollectionView.selected_forecast.attributes.forecast_date);

            let lead_time = floodCollectionView.selected_forecast.attributes.lead_time;
            let event_status = 'Current';
            if(floodCollectionView.selected_forecast.attributes.is_historical){
                event_status = 'Historical'
            }
            $(that.general_summary).html(general_template({
                flood_name: floodCollectionView.selected_forecast.attributes.notes,
                acquisition_date: flood_acquisition_date.getDate() + ' ' + monthNames[flood_acquisition_date.getMonth()] + ' ' + flood_acquisition_date.getFullYear(),
                forecast_date: flood_forecast_date.getDate() + ' ' + monthNames[flood_forecast_date.getMonth()] + ' ' + flood_forecast_date.getFullYear(),
                source: floodCollectionView.selected_forecast.attributes.source,
                notes: floodCollectionView.selected_forecast.attributes.notes,
                link: floodCollectionView.selected_forecast.attributes.link,
                lead_time: lead_time + ' Day(s)',
                event_status: event_status
            }));
            $('#vulnerability-score').html(that.loading_template);
            $('#building-count').html(that.loading_template);
            $('#vulnerability-score-road').html(that.loading_template);
            $('#road-count').html(that.loading_template);
            this.changeStatus(floodCollectionView.selected_forecast.attributes.trigger_status);
            if(callback){
                callback();
            }
        },
        renderRegionSummary: function (overall, data, main_panel, sub_region, id_field, exposure_name) {
            // main panel title (the region)
            let that = this;
            let id_key = {
                'district': 'district_id',
                'sub_district': 'sub_district_id',
                'village': 'village_id'
            };
            let trigger_status = $("#status").attr('data-region-trigger-status');
            let region = overall['region'];
            if (main_panel) {
                $('.btn-back-summary-panel').hide();
                let referer = {
                    region: 'district',
                    id: 'main',
                    trigger_status: trigger_status
                };
                if (!that.containsReferer(referer, that.referer_region)) {
                    that.referer_region.push(referer);
                }
                $('#main-panel-header').html('Summary for Flood ' + floodCollectionView.selected_forecast.attributes.notes)
            } else {
                $('.btn-back-summary-panel').show();
                let referer = {
                    region: region,
                    id: overall[id_key[region]],
                    trigger_status: trigger_status
                };
                if (referer.id !== undefined && !that.containsReferer(referer, that.referer_region)) {
                    that.referer_region.push(referer);
                }
                $('#main-panel-header').html('Summary For ' + toTitleCase(region.replace('_', ' ')) + ' ' + overall["name"])
            }
            // register stats_data
            if(data.length > 0) {
                this.panel_handlers_hash[exposure_name].stats_data = data;
            }
            else {
                // put array of undefined value, because stats_data is empty
                this.panel_handlers_hash[exposure_name].stats_data = [undefined];
            }
            // sub region summary
            // only populate sub region summary when all data has completely fetched
            let $wrapper = $('#region-summary-panel');
            if(sub_region === undefined){
                // nothing to render
                $wrapper.html('');
                return;
            }
            let is_data_ready = true;
            for(let i in this.panel_handlers){
                let handler = this.panel_handlers[i];
                if(handler.stats_data.length === 0){
                    is_data_ready = false;
                    break;
                }
            }
            if(is_data_ready){
                let title = this.sub_region_title_template;
                let item_template = this.sub_region_item_template;
                let $table = $('<table></table>');
                let pivot_data = this.panel_handlers_hash['population'].stats_data;
                if (!pivot_data[0]) {
                    $.each(this.panel_handlers_hash, function( key, value ) {
                        if(value.stats_data[0]) {
                            pivot_data = value.stats_data
                        }
                    });
                }
                console.log('test')
                // We use population data as pivot because it always represents intersected admin boundaries
                // If guarantees that this is a set of intersected admin boundaries with hazard
                for(let u=0; u<pivot_data.length; u++){
                    let item = pivot_data[u];
                    if (!item) {
                        continue
                    }
                    let trigger_status = item.trigger_status || 0;
                    $table.append(item_template({
                        region: sub_region,
                        id: item[id_field],
                        name: item['name'],
                        loading_template: that.loading_template,
                        flooded_road_count: that.loading_template,
                        flooded_building_count: that.loading_template,
                        flooded_population_count: that.loading_template,
                        trigger_status: trigger_status
                    }));
                }
                $wrapper.html(title({
                    region: toTitleCase(sub_region.replace('_', ''))
                }));
                $wrapper.append($table);
                for(let i in this.panel_handlers){
                    let handler = this.panel_handlers[i];
                    dispatcher.trigger(
                        'dashboard:inject-exposed-region-summary',
                        handler.stats_data, sub_region, id_field, handler.panelKey());
                }
            }
        },
        injectExposedRegionSummary: function(data, region, id_field, exposure_name){
            let $wrapper = $('#region-summary-panel');
            for(let u=0; u<data.length; u++){
                let item = data[u];
                if(item === undefined){
                    // continue if there is no data for current row
                    continue;
                }
                let exposed_count = item[`flooded_${exposure_name}_count`];
                let total_score = exposed_count ? exposed_count : '-';
                let $el = $wrapper.find(`[data-region-id=${item[id_field]}] .score.${exposure_name}`);
                $el.html(total_score);
            }
            // set count to 0 for every row that was not updated.
            $wrapper.find(`.score.${exposure_name} i.fa`).parent().map((idx, $el) => $($el).html(0));
        },
        changeStatus: function (status) {
            status = status || 0;
            $(this.status_wrapper).html(this.status_text[status].toUpperCase() + '!');
            $('#status').removeClass().addClass(`trigger-status-${status}`).attr('data-region-trigger-status', status);
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
        drilldown: function (e) {
            let that = this;
            let $button = $(e.target).closest('.drilldown');
            let region = $button.attr('data-region');
            let region_id = parseInt($button.attr('data-region-id'));
            let trigger_status = $button.attr('data-region-trigger-status');
            this.panel_handlers.map(o => o.stats_data = []);
            $('.btn-back-summary-panel')
                .attr('data-region', that.referer_region[that.referer_region.length - 1].region)
                .attr('data-region-id', that.referer_region[that.referer_region.length -1].id)
                .attr('data-region-trigger-status', that.referer_region[that.referer_region.length -1].trigger_status);
            this.changeStatus(trigger_status);
            dispatcher.trigger('flood:fetch-stats-data', region, region_id, false);
            dispatcher.trigger('flood:fetch-stats-data-road', region, region_id, false);
            dispatcher.trigger('flood:fetch-stats-data-population', region, region_id, false);
            this.fetchExtent(region_id, region);
            let forecast_id = floodCollectionView.selected_forecast.id;
            dispatcher.trigger('map:show-exposed-roads', forecast_id, region, region_id);
            dispatcher.trigger('map:show-region-boundary', region, region_id);
            dispatcher.trigger('map:show-exposed-buildings', forecast_id, region, region_id);
            $('#accordion').animate({
              scrollTop: 0
            }, 0)
        },
        backPanelDrilldown: function (e) {
            let that = this;
            this.referer_region.pop();

            let $button = $(e.target).closest('.btn-back-summary-panel');
            let region = $button.attr('data-region');
            let region_id = $button.attr('data-region-id');
            let trigger_status = $button.attr('data-region-trigger-status');
            let main = false;
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
            dispatcher.trigger('flood:fetch-stats-data', region, region_id, main);
            dispatcher.trigger('flood:fetch-stats-data-road', region, region_id, main);
            dispatcher.trigger('flood:fetch-stats-data-population', region, region_id, main);
            this.fetchExtent(region_id, region);
            let forecast_id = floodCollectionView.selected_forecast.id;
            dispatcher.trigger('map:show-exposed-roads', forecast_id, region, region_id);
            dispatcher.trigger('map:show-region-boundary', region, region_id);
            dispatcher.trigger('map:show-exposed-buildings', forecast_id, region, region_id);
        },
        containsReferer: function (obj, list) {
            var i;
            for (i = 0; i < list.length; i++) {
                if (list[i].region === obj.region && list[i].id === obj.id) {
                    return true;
                }

                if (list[i].region === obj.region && list[i].id !== 'main') {
                    return true;
                }
            }

            return false;
        },
        downloadSpreadsheet: function (data) {
            const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
                const byteCharacters = atob(b64Data);
                const byteArrays = [];

                for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                const slice = byteCharacters.slice(offset, offset + sliceSize);

                const byteNumbers = new Array(slice.length);
                for (let i = 0; i < slice.length; i++) {
                  byteNumbers[i] = slice.charCodeAt(i);
                }

                const byteArray = new Uint8Array(byteNumbers);
                byteArrays.push(byteArray);
                }

                const blob = new Blob(byteArrays, {type: contentType});
                return blob;
            };

            let type = 'application/vnd.ms-excel';
            const blob = b64toBlob(data, type);
            saveAs(blob, floodCollectionView.selected_forecast.attributes.notes + ".xlsx");

        },
        fetchExcel: function (){
            let that = this;
            const modal = $('#fbf-modal');
            let $loadingIcon = $('.download-spreadsheet-loading');
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
        fetchExtent: function (region_id, region) {
            if(!region_id || !region){
                return []
            }

            if(region_id === 'main'){
                dispatcher.trigger('map:fit-forecast-layer-bounds', floodCollectionView.selected_forecast)
            }

            $.get({
                url: postgresUrl + `vw_${region}_extent?id_code=eq.${region_id}`,
                success: function (data) {
                    if(data.length > 0) {
                        let coordinates = [[data[0].y_min, data[0].x_min], [data[0].y_max, data[0].x_max]];
                        dispatcher.trigger('map:fit-bounds', coordinates)
                    }
            }});
        },
        switchTab: function (e) {
            let $div = $(e.target).closest('.tab-title');
            if(!$div.hasClass('tab-active')) {
                $('.tab-wrapper').hide();
                $('.tab-title').removeClass('tab-active').removeClass('col-lg-6');
                $('.tab-title').each(function () {
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
        }
    })
});

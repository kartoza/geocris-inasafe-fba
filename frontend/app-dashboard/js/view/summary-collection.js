define([
    'backbone',
    'underscore',
    'moment',
    'leaflet',
    'wellknown',
    'utils',
    'js/model/forecast_event.js',
    'js/model/trigger_status.js',
    'js/model/hazard.js',
    'js/model/overall_summary.js',
], function (Backbone, _, moment, L, Wellknown, utils, ForecastEvent, TriggerStatusCollection, HazardCollection,
             OverallSummaryCollection) {
    return Backbone.View.extend({
        el: '.panel-browse-flood',
        forecasts_list: [],
        historical_forecasts_list: [],
        event_date_hash: {},
        selected_flood: null,
        building_type: {},
        flood_collection: null,
        flood_on_date: null,
        displayed_flood: null,
        flood_dates: [],
        districtStats: null,
        subDistrictStats: null,
        areaLookup: null,
        fetchedDate: {},
        events: {
            'click #prev-date': 'clickNavigateForecast',
            'click #next-date': 'clickNavigateForecast',
            'mouseleave': 'onFocusOut',
            'blur': 'onFocusOut'
        },
        legend: [],
        keyStats: id_key,
        initialize: function () {
            // jquery element
            this.$flood_info = this.$el.find('.flood-info');
            this.$prev_date_arrow = this.$el.find('#prev-date');
            this.$next_date_arrow = this.$el.find('#next-date');
            this.$datepicker_browse = this.$el.find('#date-browse-flood');
            this.$forecast_arrow_up = this.$el.find('.browse-arrow.arrow-up');
            this.$forecast_arrow_down = this.$el.find('.browse-arrow.arrow-down');
            this.$hide_browse_flood = this.$el.find('.hide-browse-flood');
            this.$flood_summary = $('#flood-summary');
            this.$date_legend = this.$el.find('#date-legend');
            this.datepicker_browse = null;

            // model instance
            this.hazards = new HazardCollection();
            this.trigger_statuses = new TriggerStatusCollection();
            this.stats_summaries = new OverallSummaryCollection();

            // dispatcher registration
            dispatcher.on('flood:fetch-forecast-collection', this.fetchForecastCollection, this);
            dispatcher.on('flood:update-forecast-collection', this.initializeDatePickerBrowse, this);
            dispatcher.on('flood:fetch-forecast', this.fetchForecast, this);
            dispatcher.on('flood:fetch-stats-data', this.fetchStatisticData, this);
            dispatcher.on('flood:deselect-forecast', this.deselectForecast, this);
            dispatcher.on('flood:fetch-historical-forecast', this.fetchHistoricalForecastCollection, this);
            dispatcher.on('hazard:fetch-hazard-event-summary', this.fetchHazardEventSummary, this)


            // get forecast collections
            // this.initializeTriggerStatusLegend();

            // Get recent hazard events
            this.initializeRecentHazard();

        },
        initializeRecentHazard: function () {
            const that = this;
            that.hazards.fetch()
                .then(function (data) {
                    that.$flood_summary.html(`<div class="recent-hazard-title">RECENT FORECAST</div>`);
                    let hazardListTemplate = _.template($('#hazard-list').html());
                    data.forEach(function (value) {
                        that.$flood_summary.append(hazardListTemplate(value));
                    });
                })

        },
        initializeTriggerStatusLegend: function(){
            // get trigger status_legend
            const that = this;
            this.trigger_statuses.fetch()
                .then(function (data) {
                    // render legend
                    let html = '<table class="legend">';
                    data.forEach((value) => {
                        html += '<tr>';
                        if (value.id !== 3) {
                            html += `<td><span class="colour trigger-status-${value.id}"></span><span>${value.name.capitalize()}</span></td>`;
                            html += `<td><span class="colour trigger-status-historical trigger-status-${value.id}"></span><span>Historical ${value.name.capitalize()}</span></td>`;
                            if (value.id !== 0) {
                                that.$flood_summary.prepend(
                                    `<div class="flood-count trigger-status-${value.id}" style="display: none"><span id="flood-summary-trigger-status-${value.id}"><i class="fa fa-spinner fa-spin fa-fw"></i></span> ${value.name.capitalize()} event(s)</div>`);
                            }
                        }
                        html += '</tr>';
                    });
                    html += '</table>';
                    that.$date_legend.html('<div>'+html+'</div>');
                })
                .always(function () {
                    that.fetchForecastCollection();
                    that.fetchRecentForecastEvents();

                    // fetch historical forecast to 2 months back
                    // let today = moment();
                    // previous_months = today.clone().subtract(2, 'months');
                    // that.fetchHistoricalForecastCollection(previous_months, today);
                });
        },
        initializeDatePickerBrowse: function (predefined_event) {
            const that = this;
            if (this.datepicker_browse) {
                // we need to recreate datepicker
                // because the forecast lists has changed
                this.datepicker_browse.destroy();
            }
            this.$datepicker_browse.datepicker({
                language: 'en',
                autoClose: true,
                dateFormat: 'dd/mm/yyyy',
                inline: true,
                onRenderCell: function (date, cellType) {
                    let date_string = moment(date).formatDate();
                    let event = that.event_date_hash[date_string];
                    if (cellType === 'day' && event) {
                        let classes = 'flood-date trigger-status-' + (event.trigger_status_id ? event.trigger_status_id : 0);
                        if (event.is_historical) {
                            classes += ' trigger-status-historical';
                        }
                        return {
                            classes: classes,
                        };
                    } else {
                        return {
                            classes: 'disabled',
                        };
                    }
                },
                onChangeMonth: function (month, year) {
                    // fetch historical forecast to 2 months back
                    let month_start = new moment();
                    month_start.year(year);
                    month_start.month(month - 2);
                    month_start.day(1);
                    let month_end = month_start.clone().add(3, 'month');
                    that.fetchHistoricalForecastCollection(month_start, month_end);
                },
                onSelect: function (fd, date) {
                    if (date) {
                        that.fetchForecast(date);
                    } else {
                        // empty date or deselected;
                        that.deselectForecast();
                    }
                },
                onHide: function (inst) {
                    that.is_browsing = false;
                },
                onShow: function (inst, animationCompleted) {
                    that.is_browsing = true;
                }
            });

            // change message
            this.$datepicker_browse.val('Select forecast date');
            this.datepicker_browse = this.$datepicker_browse.data('datepicker');
            if(predefined_event){
                that.fetchForecast(predefined_event.forecast_date, predefined_event.id)
            }
        },
        updateDatePicker: function(){
            if(this.datepicker_browse){
                this.datepicker_browse.update();
            }
            else {
                // try next update
                setInterval(this.updateDatePicker, 500);
            }
        },
        fetchRecentForecastEvents: function () {
            ForecastEvent.getRecentForecastList().then(
                data => {
                    console.log(data);
                }
            )
        },
        fitToHazardExtent: function (hazard) {
            let coordinates = [[hazard.extent.y_min, hazard.extent.x_min], [hazard.extent.y_max, hazard.extent.x_max]];
            dispatcher.trigger('map:fit-bounds', coordinates)
        },
        fetchHazardEventSummary: function (hazardId) {
            const that = this;
            const hazard = that.hazards.get(hazardId);
            if (typeof hazard === 'undefined') {
                console.error('Hazard could not be found');
                return false;
            }
            if (!hazard.extent) {
                hazard.fetchExtent().then(
                    function (extent) {
                        hazard.extent = extent;
                        that.fitToHazardExtent(hazard);
                        that.selectHazard(hazard);
                    }
                )
            } else {
                that.fitToHazardExtent(hazard);
                that.selectHazard(hazard);
            }
        },
        selectHazard: function (hazard) {
            this.selected_forecast = hazard;
            dispatcher.trigger('map:draw-forecast-layer', hazard)
            dispatcher.trigger('side-panel:open-dashboard')
        },
        fetchHistoricalForecastCollection: function(forecast_date_range_start, forecast_date_range_end){
            const today = moment().momentDateOnly().utc();
            const that = this;

            if(forecast_date_range_end.isAfter(today)){
                // Do not fetch historical context for dates after today.
                forecast_date_range_end = today;
            }

            ForecastEvent.getHistoricalForecastList(forecast_date_range_start, forecast_date_range_end)
                .then(function (data) {

                    data = data.map(function (value) {
                        value.is_historical = true
                        return value;
                    });

                    that.historical_forecasts_list = that.historical_forecasts_list.concat(data);

                    let date_hash = data.map(function (value) {
                        let date_string = value.forecast_date.local().formatDate();
                        return {
                            [date_string]: value
                        };
                    }).reduce(function (accumulator, value) {
                        _.extend(accumulator, value);
                        return accumulator;
                    }, {});

                    _.extend(that.event_date_hash, date_hash);


                    // update datepicker
                    that.updateDatePicker();
                })

        },
        fetchForecastCollection: function (predefined_event) {
            const today = moment().utc();
            const that = this;

            // Get flood forecast collection
            ForecastEvent.getCurrentForecastList(today)
                .then(function(data){

                    that.forecasts_list = data;

                    // create date hash for easier indexing
                    let date_hash = data.map(function (value) {
                        let date_string = value.forecast_date.local().formatDate();
                        return {
                            [date_string]: value
                        };
                    }).reduce(function (accumulator, value) {
                        _.extend(accumulator, value);
                        return accumulator;
                    }, {});

                    _.extend(that.event_date_hash, date_hash);

                    dispatcher.trigger('flood:update-forecast-collection', predefined_event);
                    that.updateForecastsSummary();
                    that.getListCentroid()
            })
        },
        updateForecastsSummary: function(){
            let flood_summary = {
                [TriggerStatusCollection.constants.NOT_ACTIVATED]: 0,
                [TriggerStatusCollection.constants.PRE_ACTIVATION]: 0,
                [TriggerStatusCollection.constants.ACTIVATION]: 0,
                all: 0
            }
            flood_summary = this.forecasts_list.reduce( function(accumulator, value) {
                let status_id = value.trigger_status_id || TriggerStatusCollection.constants.NOT_ACTIVATED;
                accumulator[status_id]++;
                accumulator.all++;
                return accumulator;
            }, flood_summary);

            _.mapObject(flood_summary, function (value, key) {
                let $element = $('#flood-summary-trigger-status-' + key);
                if ($element.length !== 0) {
                    $element.closest('.flood-count').show();
                    $element.html(parseFloat(value).numberWithCommas());
                }
                $element.addClass('flood-summary-number');
            });
        },
        updateForecastsList: function (forecasts) {
            if (forecasts.length > 1) {
                // TODO:
                // if more than one forecasts, display forecasts list
            } else {
                // TODO:
                // if only single forecast. What to display
            }
        },
        updateForecastsPager: function (current_date) {
            // check if there are previous date
            let prev_forecasts = this.forecasts_list.filter(forecast => current_date - forecast.forecast_date.local().momentDateOnly() > 0);
            // do not disable if there are previous date
            this.$prev_date_arrow.prop('disabled', !(prev_forecasts.length > 0));
            // find newest date
            if (prev_forecasts.length > 0) {
                let prev_forecast = prev_forecasts.reduce((accumulator, value) => value.forecast_date > accumulator.forecast_date ? value : accumulator, prev_forecasts[0]);
                this.$prev_date_arrow.attr('data-forecast-date', prev_forecast.forecast_date.local().formatDate());
            }
            // check if there are next date
            let next_forecasts = this.forecasts_list.filter(forecast => forecast.forecast_date.local().momentDateOnly() - current_date > 0);
            // do not disable if there are previous date
            this.$next_date_arrow.prop('disabled', !(next_forecasts.length > 0));
            // find oldest date
            if (next_forecasts.length > 0) {
                let next_forecast = next_forecasts.reduce((accumulator, value) => value.forecast_date < accumulator.forecast_date ? value : accumulator, next_forecasts[0]);
                this.$next_date_arrow.attr('data-forecast-date', next_forecast.forecast_date.local().formatDate());
            }

            // update date text
            this.$datepicker_browse.val(current_date.local().format('DD/MM/YYYY'));
        },
        selectForecast: function (forecast) {
            let that = this;
            this.selected_forecast = forecast;
            hazardTypeCollection.models.forEach(function (model) {
                if (that.selected_forecast.get('hazard_type_id') === model.get('id')){
                    that.selected_forecast.set('hazard_type', model.get('name'));
                }
            });
            dispatcher.trigger('map:draw-forecast-layer', forecast, function () {
                dispatcher.trigger('side-panel:open-dashboard', function () {
                    let callback = () => {
                        if (that.districtStats) {
                            that.fetchStatisticData('district', that.selected_forecast.id, true);
                        }
                    }
                    that.fetchDistrictData(that.selected_forecast.id, null, callback);
                });
            });

            // dispatch event to draw flood
            // change flood info
            let name = forecast.get('notes') ? forecast.get('notes') : '<i>no name</i>';
            this.$flood_info.html(`<div>${name}</div>`);
            // close browser
            this.$hide_browse_flood.click();
        },
        deselectForecast: function () {
            // when no forecast, deselect
            this.selected_forecast = null;
            this.$flood_info.empty();
            this.$datepicker_browse.val('Select forecast date');
            dispatcher.trigger('map:remove-forecast-layer');
            // close browser
            this.$hide_browse_flood.click();
        },
        fetchForecast: function (date, optional_forecast_id) {
            const that = this;
            // get event aggregate information from date string hash
            let date_string = moment(date).formatDate();
            let forecast_events_aggregate = this.event_date_hash[date_string];

            // if no forecast, do nothing
            if (!forecast_events_aggregate) {
                this.deselectForecast();
                return;
            }

            if(forecast_events_aggregate.is_historical){
                // fetch historical lists
                forecast_events_aggregate.forecast_history()
                    .then(function (data) {
                        // TODO: behaviour needs to be defined.
                        // default behaviour now is to fetch the latest
                        if (data && data.length > 0) {
                            // for now, select first forecast
                            that.selectForecast(data[0]);
                        } else {
                            that.deselectForecast();
                        }
                        that.updateForecastsList(data);
                        that.updateForecastsPager(moment(date));
                    });
            }
            else {
                // fetch current day forecast
                // fetch forecasts list for the date
                forecast_events_aggregate.available_forecasts()
                    .then(function (data) {
                        if (data && data.length > 0 && optional_forecast_id) {
                            // if forecast id specified, select that instead of first forecast.
                            data = data.filter(forecast => forecast.get('id') === optional_forecast_id);
                        }
                        if (data && data.length > 0) {
                            // for now, select first forecast
                            that.selectForecast(data[0]);
                        } else {
                            that.deselectForecast();
                        }
                        that.updateForecastsList(data);
                        that.updateForecastsPager(moment(date));
                    });
            }
        },
        onFocusOut: function (e) {
            // if(!this.is_browsing) {
            //     this.$hide_browse_flood.click();
            // }
        },
        clickNavigateForecast: function (e) {
            let date_string = $(e.currentTarget).attr('data-forecast-date');
            let selected_date = moment(date_string);
            // selecting date in date picker will trigger flood selection again.
            this.datepicker_browse.selectDate(selected_date.toJavascriptDate());
        },
        fetchStatisticData: function (region, region_id, renderRegionDetail, tab_name) {
            if (!region) {
                return []
            }

            let that = this;
            let data = {
                // TODO: add country and sub districts
                'district': that.districtStats,
                'sub_district': that.subDistrictStats
            };

            let tab_name_key = {
                'building': 'building_stats',
                'road': 'road_stats',
                'population': 'census_population_stats'
            }
            let stats_name = tab_name_key[tab_name]

            let exposure = [];
            let overall = [];
            let region_render;
            let main_panel = true;
            if (renderRegionDetail) {
                region_render = region;
                // get every exposure key and value
                data[region].map(
                    value => {
                        Object.entries(value[stats_name]).map(
                            ([key, value]) => !overall[key] ? overall[key] = value : overall[key] += value)
                    }
                )
                data[region].map((value, idx) => exposure[idx] = value[stats_name])
                dispatcher.trigger(`dashboard:render-chart-${tab_name}`, overall, tab_name);
                dispatcher.trigger('dashboard:render-region-summary', overall, exposure, main_panel, region_render, that.keyStats[region_render], tab_name, this.selected_forecast.get('hazard_type'));
            } else {
                main_panel = false;
                let sub_region = 'sub_district';
                if (region === 'sub_district') {
                    sub_region = undefined
                }
                region_render = sub_region;

                let statData = [];
                let callback = () => {
                    data = {
                        // TODO: add country and sub districts
                        'district': that.districtStats,
                        'sub_district': that.subDistrictStats
                    };
                    let parent_stat = data[region].filter(val => val[id_key[region]] === region_id)[0]
                    if(sub_region !== undefined){
                        data[sub_region].map(
                            value => {
                                Object.entries(value[stats_name]).map(
                                    ([key, value]) => !overall[key] ? overall[key] = value : overall[key] += value)
                            }
                        )
                    }
                    else {
                        Object.entries(parent_stat[stats_name]).map(
                            ([key, value]) => !overall[key] ? overall[key] = value : overall[key] += value)
                    }
                    statData = data[sub_region]
                    if(region !== 'sub_district') {
                        statData.map((value, idx) => {
                            exposure[idx] = value[stats_name];
                        })
                    }
                    name = parent_stat.name
                    overall['region'] = region;
                    overall[id_key[region]] = region_id
                    overall['name'] = name
                    dispatcher.trigger(`dashboard:render-chart-${tab_name}`, overall, tab_name);
                    dispatcher.trigger('dashboard:render-region-summary', overall, exposure, main_panel, region_render, that.keyStats[region_render], tab_name, this.selected_forecast.get('hazard_type'));
                }
                if(sub_region === 'sub_district'){
                    that.fetchSubDistrictData(that.selected_forecast.id, region_id, callback)
                }

                if(sub_region === undefined){
                    callback()
                }
            }
        },
        fetchDistrictData: function (flood_event_id, parent_id, callback) {
            let that = this;
            this.stats_summaries.id = flood_event_id
            this.stats_summaries.admin_level = 'district'
            this.stats_summaries.fetch().then(function (data) {
                that.districtStats = data;
                if(callback){
                    callback()
                }
            }).catch(function (data) {
                console.log('District stats request failed');
                console.log(data);
            });
        },
        fetchSubDistrictData: function (flood_event_id, parent_id, callback) {
            let that = this;
            this.stats_summaries.id = flood_event_id
            this.stats_summaries.admin_level = 'sub_district'
            this.stats_summaries.parent_level = 'district'
            this.stats_summaries.parent_id = parent_id
            this.stats_summaries.fetch().then(function (data) {
                that.subDistrictStats = data;
                if(callback){
                    callback()
                }
            }).catch(function (data) {
                console.log('Sub district stats request failed');
                console.log(data);
            })
        },
        getListCentroid: function () {
            dispatcher.trigger('map:remove-all-markers');
            let that = this;
            $.each(that.forecasts_list, function (index, forecast) {
                let forecast_events_aggregate = forecast;
                forecast_events_aggregate.available_forecasts()
                    .then(function (data) {
                        if (data && data.length > 0) {
                            data[0].fetchExtent().then(function (extent) {
                                let _extent = L.latLngBounds(extent.leaflet_bounds);
                                dispatcher.trigger('map:add-marker', _extent.getCenter(), forecast_events_aggregate.trigger_status_id)
                            })
                        }
                    });
            })
        }
    })
});

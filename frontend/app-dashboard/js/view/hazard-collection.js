define([
    'backbone',
    'underscore',
    'moment',
    'leaflet',
    'wellknown',
    'utils',
    'js/model/forecast_event.js',
    'js/model/trigger_status.js',
    'js/model/district_summary.js',
    'js/model/subdistrict_summary.js',
    'js/model/village_summary.js',
    'js/model/road_district_summary.js',
    'js/model/road_sub_district_summary.js',
    'js/model/road_village_summary.js',
    'js/model/population_district_summary.js',
    'js/model/population_sub_district_summary.js',
    'js/model/population_village_summary.js',
    'js/model/world_population_district_summary.js',
    'js/model/world_population_sub_district_summary.js',
    'js/model/world_population_village_summary.js',
], function (Backbone, _, moment, L, Wellknown, utils, ForecastEvent, TriggerStatusCollection,
             DistrictSummaryCollection, SubDistrictSummaryCollection, VillageSummaryCollection,
             RoadDistrictSummaryCollection, RoadSubDistrictSummaryCollection, RoadVillageSummaryCollection,
             PopulationDistrictSummaryCollection, PopulationSubDistrictSummaryCollection, PopulationVillageSummaryCollection,
             WorldPopulationDistrictSummaryCollection, WorldPopulationSubDistrictSummaryCollection, WorldPopulationVillageSummaryCollection) {
    return Backbone.View.extend({
        el: '.panel-browse-hazard',
        forecasts_list: [],
        historical_forecasts_list: [],
        event_date_hash: {},
        selected_hazard: null,
        building_type: {},
        hazard_collection: null,
        hazard_on_date: null,
        displayed_hazard: null,
        hazard_dates: [],
        villageStats: null,
        subDistrictStats: null,
        districtStats: null,
        roadVillageStats: null,
        roadSubDistrictStats: null,
        roadDistrictStats: null,
        populationVillageStats: null,
        populationSubDistrictStats: null,
        populationDistrictStats: null,
        worldPopulationVillageStats: null,
        worldPopulationSubDistrictStats: null,
        worldPopulationDistrictStats: null,
        areaLookup: null,
        fetchedDate: {},
        events: {
            'click #prev-date': 'clickNavigateForecast',
            'click #next-date': 'clickNavigateForecast',
            'mouseleave': 'onFocusOut',
            'blur': 'onFocusOut'
        },
        legend: [],
        keyStats: {
            'district': 'district_id',
            'sub_district': 'sub_district_id',
            'village': 'village_id'
        },
        initialize: function () {
            // jquery element
            this.$hazard_info = this.$el.find('.hazard-info');
            this.$prev_date_arrow = this.$el.find('#prev-date');
            this.$next_date_arrow = this.$el.find('#next-date');
            this.$datepicker_browse = this.$el.find('#date-browse-hazard');
            this.$forecast_arrow_up = this.$el.find('.browse-arrow.arrow-up');
            this.$forecast_arrow_down = this.$el.find('.browse-arrow.arrow-down');
            this.$hide_browse_hazard = this.$el.find('.hide-browse-hazard');
            this.$hazard_summary = $('#hazard-summary');
            this.$date_legend = this.$el.find('#date-legend');
            this.datepicker_browse = null;

            // model instance
            this.trigger_statuses = new TriggerStatusCollection();
            this.village_summaries = new VillageSummaryCollection();
            this.district_summaries = new DistrictSummaryCollection();
            this.subdistrict_summaries = new SubDistrictSummaryCollection();
            this.road_village_summaries = new RoadVillageSummaryCollection();
            this.road_district_summaries = new RoadDistrictSummaryCollection();
            this.road_subdistrict_summaries = new RoadSubDistrictSummaryCollection();
            this.population_village_summaries = new PopulationVillageSummaryCollection();
            this.population_district_summaries = new PopulationDistrictSummaryCollection();
            this.population_subdistrict_summaries = new PopulationSubDistrictSummaryCollection();
            this.world_population_village_summaries = new WorldPopulationVillageSummaryCollection();
            this.world_population_district_summaries = new WorldPopulationDistrictSummaryCollection();
            this.world_population_subdistrict_summaries = new WorldPopulationSubDistrictSummaryCollection();

            // dispatcher registration
            dispatcher.on('hazard:fetch-forecast-collection', this.fetchForecastCollection, this);
            dispatcher.on('hazard:update-forecast-collection', this.initializeDatePickerBrowse, this);
            dispatcher.on('hazard:fetch-forecast', this.fetchForecast, this);
            dispatcher.on('hazard:fetch-stats-data', this.fetchStatisticData, this);
            dispatcher.on('hazard:fetch-stats-data-road', this.fetchRoadStatisticData, this);
            dispatcher.on('hazard:fetch-stats-data-population', this.fetchPopulationStatisticData, this);
            dispatcher.on('hazard:deselect-forecast', this.deselectForecast, this);
            dispatcher.on('hazard:fetch-historical-forecast', this.fetchHistoricalForecastCollection, this);


            // get forecast collections
            this.initializeTriggerStatusLegend();

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
                                that.$hazard_summary.prepend(
                                    `<div class="hazard-count trigger-status-${value.id}" style="display: none"><span id="hazard-summary-trigger-status-${value.id}"><i class="fa fa-spinner fa-spin fa-fw"></i></span> ${value.name.capitalize()} event(s)</div>`);
                            }
                        }
                        html += '</tr>';
                    });
                    html += '</table>';
                    that.$date_legend.html('<div>'+html+'</div>');
                })
                .always(function () {
                    that.fetchForecastCollection();

                    // fetch historical forecast to 2 months back
                    let today = moment();
                    previous_months = today.clone().subtract(2, 'months');
                    that.fetchHistoricalForecastCollection(previous_months, today);
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
                        let classes = 'hazard-date trigger-status-' + (event.trigger_status_id ? event.trigger_status_id : 0);
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

            // Get hazard forecast collection
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

                    dispatcher.trigger('hazard:update-forecast-collection', predefined_event);
                    that.updateForecastsSummary();
                    that.getListCentroid()
            })
        },
        updateForecastsSummary: function(){
            let hazard_summary = {
                [TriggerStatusCollection.constants.NOT_ACTIVATED]: 0,
                [TriggerStatusCollection.constants.PRE_ACTIVATION]: 0,
                [TriggerStatusCollection.constants.ACTIVATION]: 0,
                all: 0
            }
            hazard_summary = this.forecasts_list.reduce( function(accumulator, value) {
                let status_id = value.trigger_status_id || TriggerStatusCollection.constants.NOT_ACTIVATED;
                accumulator[status_id]++;
                accumulator.all++;
                return accumulator;
            }, hazard_summary);

            _.mapObject(hazard_summary, function (value, key) {
                let $element = $('#hazard-summary-trigger-status-' + key);
                if ($element.length !== 0) {
                    $element.closest('.hazard-count').show();
                    $element.html(value);
                }
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
            dispatcher.trigger('map:draw-forecast-layer', forecast, function () {
                dispatcher.trigger('side-panel:open-dashboard', function () {
                    that.fetchVillageData(that.selected_forecast.id);
                    that.fetchSubDistrictData(that.selected_forecast.id);
                    that.fetchDistrictData(that.selected_forecast.id);
                    that.fetchRoadVillageData(that.selected_forecast.id);
                    that.fetchRoadSubDistrictData(that.selected_forecast.id);
                    that.fetchRoadDistrictData(that.selected_forecast.id);
                    that.fetchPopulationVillageData(that.selected_forecast.id);
                    that.fetchPopulationSubDistrictData(that.selected_forecast.id);
                    that.fetchPopulationDistrictData(that.selected_forecast.id);
                });
            });

            // dispatch event to draw hazard
            // change hazard info
            let name = forecast.get('notes') ? forecast.get('notes') : '<i>no name</i>';
            this.$hazard_info.html(`<div>${name}</div>`);
            // close browser
            this.$hide_browse_hazard.click();
        },
        deselectForecast: function () {
            // when no forecast, deselect
            this.selected_forecast = null;
            this.$hazard_info.empty();
            this.$datepicker_browse.val('Select forecast date');
            dispatcher.trigger('map:remove-forecast-layer');
            // close browser
            this.$hide_browse_hazard.click();
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
            //     this.$hide_browse_hazard.click();
            // }
        },
        clickNavigateForecast: function (e) {
            let date_string = $(e.currentTarget).attr('data-forecast-date');
            let selected_date = moment(date_string);
            // selecting date in date picker will trigger hazard selection again.
            this.datepicker_browse.selectDate(selected_date.toJavascriptDate());
        },
        fetchStatisticData: function (region, region_id, renderRegionDetail) {
            if (!region) {
                return []
            }

            let that = this;
            let data = {
                'village': that.villageStats,
                'district': that.districtStats,
                'sub_district': that.subDistrictStats
            };

            let buildings = [];
            let overall = [];
            let region_render;
            let main_panel = true;
            if (renderRegionDetail) {
                region_render = region;
                $.each(data[region], function (idx, value) {
                    buildings[idx] = [];
                    $.each(value, function (key, value) {
                        buildings[idx][key] = value;
                        if (!overall[key]) {
                            overall[key] = value
                        } else {
                            overall[key] += value
                        }
                    })
                });
                if (overall.hasOwnProperty('police_hazarded_building_count')) {
                    overall['police_station_hazarded_building_count'] = overall['police_hazarded_building_count'];
                    delete overall['police_hazarded_building_count'];
                }
                delete overall['region_id'];
                delete overall[region + '_id'];
                delete overall['name'];
                delete overall['village_id'];
                delete overall['sub_district_id'];
                delete overall['district_id'];
                delete overall['trigger_status'];
            } else {
                main_panel = false;
                let sub_region = 'sub_district';
                if (region === 'sub_district') {
                    sub_region = 'village'
                }
                if (region === 'village'){
                    sub_region = undefined;
                }
                region_render = sub_region;

                let statData = [];
                let subRegionList = that.getListSubRegion(sub_region, region_id, data);
                $.each(data[sub_region], function (index, value) {
                    if (subRegionList.indexOf(value[that.keyStats[sub_region]]) >= 0) {
                        statData.push(value)
                    }
                });

                if (region !== 'village') {
                    $.each(statData, function (idx, value) {
                        buildings[idx] = [];
                        $.each(value, function (key, value) {
                            if (key === 'police_hazarded_building_count') {
                                key = 'police_station_hazarded_building_count'
                            }
                            buildings[idx][key] = value;
                        })
                    });
                }

                for (let index = 0; index < data[region].length; index++) {
                    if (data[region][index][that.keyStats[region]] === parseInt(region_id)) {
                        overall = data[region][index];
                        if (overall.hasOwnProperty('police_hazarded_building_count')) {
                            overall['police_station_hazarded_building_count'] = overall['police_hazarded_building_count'];
                            delete overall['police_hazarded_building_count'];
                        }
                        break
                    }
                }
                overall['region'] = region;
            }
            dispatcher.trigger('dashboard:render-chart-building', overall, 'building');
            dispatcher.trigger('dashboard:render-region-summary', overall, buildings, main_panel, region_render, that.keyStats[region_render], 'building');
        },
        fetchVillageData: function (hazard_event_id) {
            let that = this;
            this.village_summaries.fetch({
                data: {
                    hazard_event_id: `eq.${hazard_event_id}`,
                    order: 'trigger_status.desc,total_vulnerability_score.desc'
                }
            }).then(function (data) {
                that.villageStats = data;
                if (that.villageStats !== null && that.districtStats !== null && that.subDistrictStats !== null) {
                    that.fetchStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                    console.log('Village stats request failed');
                    console.log(data)
            });
        },
        fetchDistrictData: function (hazard_event_id) {
            let that = this;
            this.district_summaries.fetch({
                data: {
                    hazard_event_id: `eq.${hazard_event_id}`,
                    order: 'trigger_status.desc,total_vulnerability_score.desc'
                }
            }).then(function (data) {
                that.districtStats = data;
                if (that.villageStats !== null && that.districtStats !== null && that.subDistrictStats !== null) {
                    that.fetchStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                console.log('District stats request failed');
                console.log(data);
            });
        },
        fetchSubDistrictData: function (hazard_event_id) {
            let that = this;
            this.subdistrict_summaries.fetch({
                data: {
                    hazard_event_id: `eq.${hazard_event_id}`,
                    order: 'trigger_status.desc,total_vulnerability_score.desc'
                }
            }).then(function (data) {
                that.subDistrictStats = data;
                if (that.villageStats !== null && that.districtStats !== null && that.subDistrictStats !== null) {
                    that.fetchStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                console.log('Sub district stats request failed');
                console.log(data);
            })
        },
        getListSubRegion: function (region, parent_region_id, stats) {
            let key = {
                'sub_district': 'sub_district_id',
                'village': 'village_id'
            };
            let keyParent = {
                'sub_district': 'district_id',
                'village': 'sub_district_id'
            };
            let that = this;
            let areaLookup = stats[region]
            let listSubRegion = [];
            $.each(areaLookup, function (index, value) {
                if (parseInt(value[keyParent[region]]) === parseInt(parent_region_id)) {
                    listSubRegion.push(value[key[region]])
                }
            });
            return listSubRegion
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
        },
        fetchRoadStatisticData: function (region, region_id, renderRegionDetail) {
            if (!region) {
                return []
            }

            let that = this;
            let data = {
                'village': that.roadVillageStats,
                'district': that.roadDistrictStats,
                'sub_district': that.roadSubDistrictStats
            };

            let roads = [];
            let overall = [];
            let region_render;
            let main_panel = true;
            if (renderRegionDetail) {
                region_render = region;
                $.each(data[region], function (idx, value) {
                    roads[idx] = [];
                    $.each(value, function (key, value) {
                        roads[idx][key] = value;
                        if (!overall[key]) {
                            overall[key] = value
                        } else {
                            overall[key] += value
                        }
                    })
                });
                delete overall['region_id'];
                delete overall[region + '_id'];
                delete overall['name'];
                delete overall['village_id'];
                delete overall['sub_district_id'];
                delete overall['district_id'];
                delete overall['trigger_status'];
            } else {
                let sub_region = 'sub_district';
                if (region === 'sub_district') {
                    sub_region = 'village'
                }
                if (region === 'village'){
                    sub_region = undefined;
                }
                region_render = sub_region;
                main_panel = false;

                let statData = [];
                let subRegionList = that.getListSubRegion(sub_region, region_id, data);
                $.each(data[sub_region], function (index, value) {
                    if (subRegionList.indexOf(value[that.keyStats[sub_region]]) >= 0) {
                        statData.push(value)
                    }
                });

                if (region !== 'village') {
                    $.each(statData, function (idx, value) {
                        roads[idx] = [];
                        $.each(value, function (key, value) {
                            roads[idx][key] = value;
                        })
                    });
                }

                for (let index = 0; index < data[region].length; index++) {
                    if (data[region][index][that.keyStats[region]] === parseInt(region_id)) {
                        overall = data[region][index];
                        break
                    }
                }
                overall['region'] = region;
            }
            dispatcher.trigger('dashboard:render-chart-road', overall, 'road');
            dispatcher.trigger('dashboard:render-region-summary', overall, roads, main_panel, region_render, that.keyStats[region_render], 'road');
        },
        fetchRoadDistrictData: function (hazard_event_id) {
            let that = this;
            this.road_district_summaries.fetch({
                data: {
                    hazard_event_id: `eq.${hazard_event_id}`,
                    order: 'trigger_status.desc,total_vulnerability_score.desc'
                }
            }).then(function (data) {
                that.roadDistrictStats = data;
                if (that.roadVillageStats !== null && that.roadDistrictStats !== null && that.roadSubDistrictStats !== null) {
                    that.fetchRoadStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                console.log('District stats request failed');
                console.log(data);
            });
        },
        fetchRoadSubDistrictData: function (hazard_event_id) {
            let that = this;
            this.road_subdistrict_summaries.fetch({
                data: {
                    hazard_event_id: `eq.${hazard_event_id}`,
                    order: 'trigger_status.desc,total_vulnerability_score.desc'
                }
            }).then(function (data) {
                that.roadSubDistrictStats = data;
                if (that.roadVillageStats !== null && that.roadDistrictStats !== null && that.roadSubDistrictStats !== null) {
                    that.fetchRoadStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                console.log('Sub district stats request failed');
                console.log(data);
            })
        },
        fetchRoadVillageData: function (hazard_event_id) {
            let that = this;
            this.road_village_summaries.fetch({
                data: {
                    hazard_event_id: `eq.${hazard_event_id}`,
                    order: 'trigger_status.desc,total_vulnerability_score.desc'
                }
            }).then(function (data) {
                that.roadVillageStats = data;
                if (that.roadVillageStats !== null && that.roadDistrictStats !== null && that.roadSubDistrictStats !== null) {
                    that.fetchRoadStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                    console.log('Village stats request failed');
                    console.log(data)
            });
        },
        fetchPopulationStatisticData: function (region, region_id, renderRegionDetail) {
            if (!region) {
                return []
            }

            let that = this;
            let data = {
                'village': that.populationVillageStats,
                'district': that.populationDistrictStats,
                'sub_district': that.populationSubDistrictStats
            };

            let population = [];
            let overall = [];
            let region_render;
            let main_panel = true;
            if (renderRegionDetail) {
                region_render = region;
                $.each(data[region], function (idx, value) {
                    population[idx] = [];
                    $.each(value, function (key, value) {
                        population[idx][key] = value;
                        if (!overall[key]) {
                            overall[key] = value
                        } else {
                            overall[key] += value
                        }
                    })
                });
                delete overall['region_id'];
                delete overall[region + '_id'];
                delete overall['name'];
                delete overall['village_id'];
                delete overall['sub_district_id'];
                delete overall['district_id'];
                delete overall['trigger_status'];
            } else {
                let sub_region = 'sub_district';
                if (region === 'sub_district') {
                    sub_region = 'village'
                }
                if(region === 'village'){
                    sub_region = undefined;
                }
                region_render = sub_region;
                main_panel = false;

                let statData = [];
                let subRegionList = that.getListSubRegion(sub_region, region_id, data);
                $.each(data[sub_region], function (index, value) {
                    if (subRegionList.indexOf(value[that.keyStats[sub_region]]) >= 0) {
                        statData.push(value)
                    }
                });

                if (region !== 'village') {
                    $.each(statData, function (idx, value) {
                        population[idx] = [];
                        $.each(value, function (key, value) {
                            population[idx][key] = value;
                        })
                    });
                }

                for (let index = 0; index < data[region].length; index++) {
                    if (data[region][index][that.keyStats[region]] === parseInt(region_id)) {
                        overall = data[region][index];
                        break
                    }
                }
                overall['region'] = region;
            }
            dispatcher.trigger('dashboard:render-chart-population', overall, 'population');
            dispatcher.trigger('dashboard:render-region-summary', overall, population, main_panel, region_render, that.keyStats[region_render], 'population');
        },
        _merge_population_stats: function(hazard_event_id, stats_data, stats_collections, region){
            let that = this;
            let region_id = `${region}_id`;
            let stats_promises = stats_collections.map((o, i) => o.fetch({
                    data: {
                        hazard_event_id: `eq.${hazard_event_id}`,
                        order: 'trigger_status.desc,hazarded_population_count.desc'
                    }
                }));
            Promise.all(stats_promises).then(function (data) {
                // merge data from world pop to census population
                // merge is done by region_id key
                let merged_pop_data = [];
                let base_data = data[0]
                let extra_data = data[1]
                while(base_data.length > 0){
                    let base_stat = base_data.pop();
                    let matching_extra_stat_index = extra_data.findIndex( s => s[region_id] === base_stat[region_id]);
                    let matching_extra_stat = extra_data[matching_extra_stat_index];
                    if(matching_extra_stat_index > -1) {
                        extra_data.splice(matching_extra_stat_index, 1);
                    }
                    // mark population count of census as a census_count key
                    base_stat['census_count'] = base_stat['hazarded_population_count'];
                    delete base_stat['hazarded_population_count'];
                    delete base_stat['population_count'];
                    let merged_stat = {...base_stat, ...matching_extra_stat};
                    merged_pop_data.push(merged_stat);
                }
                // sort by affected population (descending)
                merged_pop_data.sort( (a,b) => b['hazarded_population_count'] - a['hazarded_population_count'])
                that[stats_data[0]] = merged_pop_data;
                that[stats_data[1]] = extra_data;
                if (that.populationVillageStats !== null && that.populationDistrictStats !== null && that.populationSubDistrictStats !== null) {
                    that.fetchPopulationStatisticData('district', that.selected_forecast.id, true);
                }
            }).catch(function (data) {
                console.log(`${region} stats request failed: ${stats_data[i]}`);
                console.log(data);
            });
        },
        fetchPopulationDistrictData: function (hazard_event_id) {
            let that = this;

            // Population data stats are a combined data from census population and world pop population stats
            let stats_collections = [this.population_district_summaries, this.world_population_district_summaries];
            let stats_data = ['populationDistrictStats', 'worldPopulationDistrictStats'];
            let region = 'district';
            this._merge_population_stats(hazard_event_id, stats_data, stats_collections, region);
        },
        fetchPopulationSubDistrictData: function (hazard_event_id) {
            let that = this;

            // Population data stats are a combined data from census population and world pop population stats
            let stats_collections = [this.population_subdistrict_summaries, this.world_population_subdistrict_summaries];
            let stats_data = ['populationSubDistrictStats', 'worldPopulationSubDistrictStats'];
            let region = 'sub_district';
            this._merge_population_stats(hazard_event_id, stats_data, stats_collections, region);
        },
        fetchPopulationVillageData: function (hazard_event_id) {
            let that = this;

            // Population data stats are a combined data from census population and world pop population stats
            let stats_collections = [this.population_village_summaries, this.world_population_village_summaries];
            let stats_data = ['populationVillageStats', 'worldPopulationVillageStats'];
            let region = 'village';
            this._merge_population_stats(hazard_event_id, stats_data, stats_collections, region);
        }
    })
});

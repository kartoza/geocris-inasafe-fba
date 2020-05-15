define([
    'backbone',
    'jquery',
], function (Backbone, $) {

    return Backbone.View.extend({
        _panel_key: 'generic',
        stats_data: [],
        primary_exposure_key: 'residential',
        primary_exposure_label: `Residential ${this._panel_key}`,
        other_category_exposure_label: `Other ${this._panel_key}`,
        initialize: function(panel_dashboard){
            this.panel_dashboard = panel_dashboard;
        },
        reset: function(){
            this.stats_data = []
        },
        panelKey: function(){
            return this._panel_key;
        },
        renderChartElement: function (data, exposure_name) {
            exposure_name = exposure_name ? exposure_name : this.panelKey();
            let $parentWrapper = $(`#chart-score-panel .tab-${exposure_name}`);
            $parentWrapper.find('.summary-chart').remove();
            $parentWrapper.find('.panel-chart').html('<canvas class="summary-chart" style="height: 250px"></canvas>');
            $parentWrapper.find('.summary-chart-primary').remove();
            $parentWrapper.find('.panel-chart-primary').html('<canvas class="summary-chart-primary" style="height: 100px"></canvas>');

            let total_building_array = [];
            let graph_data = [];
            let hazard_graph_data = [];
            let backgroundColours = [];
            let total_hazarded_count_key = `hazarded_${exposure_name}_count`;
            let total_count_key = `${exposure_name}_count`;
            let unlisted_key = [
                'id', 'hazard_event_id', 'total_vulnerability_score', total_hazarded_count_key, total_count_key,
                'village_id', 'name', 'region', 'district_id', 'sub_district_id', 'sub_dc_code', 'village_code', 'dc_code',
                'trigger_status'
            ];
            let primary_exposure_hazard_data = [];
            let primary_exposure_data = [];
            let hazarded_count_key_suffix = `_hazarded_${exposure_name}_count`;
            let total_count_key_suffix = `_${exposure_name}_count`;
            let label = [];
            for (let key in data) {
                let is_in_unlisted = unlisted_key.indexOf(key) > -1;
                if(is_in_unlisted) { continue; }

                let is_hazarded_count = key.endsWith(hazarded_count_key_suffix);
                let is_primary_exposure = key.indexOf(this.primary_exposure_key) > -1;

                if(is_primary_exposure && is_hazarded_count){
                    // Record primary exposure data for pie chart
                    primary_exposure_hazard_data = data[key];
                    primary_exposure_data = data[key.replace(hazarded_count_key_suffix, total_count_key_suffix)];
                }
                else if(is_hazarded_count){
                    // Record hazarded data for bar chart
                    let breakdown_key = key.replace(hazarded_count_key_suffix, '');
                    let total_count_key = key.replace(hazarded_count_key_suffix, total_count_key_suffix);
                    hazard_graph_data.push({
                        y: breakdown_key,
                        x: data[key]
                    })

                    // Figure out non hazarded count
                    let non_hazarded_count = data[total_count_key] - data[key];
                    if(isNaN(non_hazarded_count)){
                        non_hazarded_count = 0;
                    }
                    graph_data.push({
                        y: breakdown_key,
                        x: non_hazarded_count
                    });

                    // Figure out total count
                    total_building_array.push({
                        key: breakdown_key,
                        value: data[total_count_key]
                    });
                }

                backgroundColours.push('#82B7CA');
            }

            // Sort descending
            total_building_array.sort(function (a, b) {
                return b.value - a.value
            });

            for(let i in total_building_array){
                let o = total_building_array[i]
                let is_primary_exposure = o.key.indexOf(this.primary_exposure_key) > -1;
                if(! is_primary_exposure){
                    label.push(o.key);
                }
            }

            graph_data.sort(function (a, b) {
                return label.indexOf(a.y) - label.indexOf(b.y);
            });

            hazard_graph_data.sort(function (a, b) {
                return label.indexOf(a.y) - label.indexOf(b.y);
            });

            let humanLabel = [];
            for (let i = 0; i < label.length; i++) {
                humanLabel.push(toTitleCase(label[i].replace('_', ' ')))
            }

            let ctxPrimaryExposure = $parentWrapper.find('.summary-chart-primary').get(0).getContext('2d');
            let datasetsPrimaryExposure = {
                labels: ["Not Affected", "Affected"],
                datasets: [{
                    data: [primary_exposure_data - primary_exposure_hazard_data, primary_exposure_hazard_data],
                    backgroundColor: ['#e5e5e5', '#82B7CA']
                }]
            };
            let ctx = $parentWrapper.find('.summary-chart').get(0).getContext('2d');
            let datasets = {
                labels: humanLabel,
                datasets: [
                    {
                        label: "Not Affected",
                        data: graph_data
                    }, {
                        label: "Affected",
                        data: hazard_graph_data,
                        backgroundColor: backgroundColours
                    }]
            };

            let is_vulnerability_score_exists = data['total_vulnerability_score'] !== undefined;
            let is_exposed_count_exists = data[total_hazarded_count_key] !== undefined;
            let $vulnerability_info = $parentWrapper.find('.vulnerability-score');
            if(is_vulnerability_score_exists){
                let total_vulnerability_score = data['total_vulnerability_score'] ? data['total_vulnerability_score'].toFixed(2) : 0;
                $vulnerability_info.html(total_vulnerability_score);
                $vulnerability_info.parent().show();
            }
            else{
                $vulnerability_info.parent().hide();
            }
            $parentWrapper.find('.exposed-count').html(is_exposed_count_exists ? data[total_hazarded_count_key] : 0);

            this.renderChartData(datasets, ctx, this.primary_exposure_label, datasetsPrimaryExposure, ctxPrimaryExposure, this.other_category_exposure_label);
        },
        renderChartData: function (datasets, ctx, title, datasetsPrimaryExposure, ctxPrimaryExposure, title2) {
            new Chart(ctxPrimaryExposure, {
                type: 'pie',
                data: datasetsPrimaryExposure,
                options: {
                    legend: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: title
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        labels: {
                            render: 'value',
                            position: 'outside',
                            textMargin: 4
                        }
                    }
                }
            });

            new Chart(ctx, {
                type: 'horizontalBar',
                data: datasets,
                options: {
                    legend: {
                        display: true
                    },
                    scales: {
                        xAxes: [{
                            stacked: true,
                            gridLines: {
                                display:false
                            },
                            ticks: {
                                min: 0
                            }
                        }],
                        yAxes: [{
                            stacked: true,
                            gridLines: {
                                display:false
                            },
                        }]
                    },
                    title: {
                        display: true,
                        text: title2
                    },
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        },
    });
});

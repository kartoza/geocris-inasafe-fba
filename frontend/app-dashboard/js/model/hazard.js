define([
    'backbone',
    'wellknown'
    ], function (Backbone, Wellknown) {

    /**
     * Attributes:
     *  - areas []
     *      - geometry
     *      - hazard_class
     *  - geojson
     *  - id
     *  - place_name
     *  - notes
     *  - return_period
     *  - station
     *      - glofas_id
     *      - name
     *      - geometry
     */
    const HazardLayer = Backbone.Model.extend({

            // attribute placeholder
            _url : {
                hazarded_area: postgresUrl + 'hazard_area',
                hazarded_areas: postgresUrl + 'hazard_areas',
                hazard_map: postgresUrl + 'hazard_map'
            },
            _table_attrs: {
                hazard_map: {
                    place_name: 'place_name',
                    notes: 'notes',
                    return_period: 'return_period'
                },
                hazarded_areas: {
                    hazard_id: 'hazard_map_id',
                    hazarded_area_id: 'hazarded_area_id'
                },
                hazarded_area: {
                    hazard_class: 'hazard_class',
                    geometry: 'geometry'
                }
            },

            _geojson_attrs: {
                hazard_class_field: "class"
            },
        
            initialize: function (){
                this._uploaded_features = 0;
                this.on('feature-uploaded', this.featureUploaded, this);
            },

            getHazardMapAttributes: function(){
                return {
                    [this._table_attrs.hazard_map.place_name]: this.get('place_name'),
                    [this._table_attrs.hazard_map.notes]: this.get('notes'),
                    [this._table_attrs.hazard_map.return_period]: this.get('return_period')
                }
            },

            featureCount: function(){
                const areas = this.get('areas');
                if(areas) {
                    return areas.length;
                }
                return 0;
            },
        
            featureUploaded: function(feature){
                if(feature) {
                    this._uploaded_features++;
                }
                if ( this._uploaded_features > this.featureCount()) {
                    this._uploaded_features = this.featureCount();
                }
            },

            uploadedFeatures: function(){
                return this._uploaded_features
            },

            _createHazardMap: function () {
                const that = this
                return new Promise(function (resolve, reject) {
                    // Create new hazard map first, then retrieve the id
                    AppRequest.post(
                        that._url.hazard_map,
                        that.getHazardMapAttributes())
                        .done( function(data, textStatus, response){
                            if(response.status === 201){
                                // Hazard map creation succeed
                                // get the hazard map id
                                const hazard_map_url = postgresBaseUrl + response.getResponseHeader('Location')
                                AppRequest.get(hazard_map_url)
                                    .done(
                                        function (data) {
                                            if (data && data[0]) {
                                                const hazard_map_id = data[0].id
                                                // Create hazarded area relationship
                                                that._createHazardedAreas(hazard_map_id)
                                                // if succeed, done
                                                    .then(function () {
                                                        resolve({
                                                            id: hazard_map_id,
                                                            url: hazard_map_url
                                                        })
                                                    })
                                                    // if fails, reject
                                                    .catch(reject)
                                            }
                                        }
                                    ).catch(reject)
                            }
                            else {
                                reject(response)
                            }
                        }).catch(reject)
                })
            },

            _createHazardedAreas: function (hazard_map_id) {
                // Bulk insert doesn't return ids, so we insert one by one
                const areas = this.get('areas')
                const that = this

                const on_post_fails = function (data) {
                    console.log(data)
                    console.log('Hazarded Area post fails: ' + data)
                }

                const on_post_relations_fails = function (data) {
                    console.log('Hazarded Area relationship post fails: ' + data)
                }

                const created_areas = areas.map(function(value){
                    // Insert hazard area, one by one, as promise.
                    return that._createHazardedArea({
                        [that._table_attrs.hazarded_area.geometry]: 'SRID=4326;' + Wellknown.stringify(value.geometry),
                        [that._table_attrs.hazarded_area.hazard_class]: value.hazard_class
                    }).catch(on_post_fails)
                })

                return new Promise(function (resolve, reject) {
                    // If all posted areas succeed, insert relationships
                    Promise.all(created_areas).then(function (values) {
                        // Make lists of Hazard_Area - Hazard_Areas relationship
                        const relations = values.map(function (value) {
                            return {
                                [that._table_attrs.hazarded_areas.hazard_id]: hazard_map_id,
                                [that._table_attrs.hazarded_areas.hazarded_area_id]: value.id
                            }
                        })
                        // Bulk insert relationship
                        AppRequest.post(
                            that._url.hazarded_areas,
                            relations,
                            null,
                            null,
                            'application/json')
                            .done(
                                function (data, textStatus, response) {
                                    if(response.status === 201) {
                                        // Bulk insert succeed
                                        // we resolve but nothing to return since the REST API doesn't have anything useful returned
                                        that.set({
                                            id: hazard_map_id
                                        })
                                        resolve()
                                    }
                                    else {
                                        // posting relationship fails
                                        on_post_relations_fails(response)
                                        // tell what the response is
                                        reject(response)
                                    }
                                })
                            // request error
                            .catch(reject)

                        // one of the promise to post hazard area fails
                    }).catch(on_post_fails)
                })
            },

            _createHazardedArea: function (area) {
                // Return promised created hazarded area object
                const that = this
                return new Promise(function (resolve, reject) {
                    // Insert an area
                    AppRequest.post(
                        that._url.hazarded_area,
                        area)
                        .done(
                            // callback to get area id
                            function (data, textStatus, response) {
                                if(response.status === 201){
                                    // get object
                                    const hazarded_area_url = postgresBaseUrl + response.getResponseHeader('Location')
                                    AppRequest.get(
                                        // created object were given via Location header
                                        hazarded_area_url,
                                        null,
                                        null,
                                        function (data) {
                                            // send the newly created object
                                            if(data && data[0]){
                                                that.trigger('feature-uploaded', data[0])
                                                resolve(data[0])
                                            }
                                            else {
                                                reject(data)
                                            }
                                        },
                                        reject
                                    )
                                }
                                else {
                                    reject(data)
                                }
                            })
                        .catch(reject)
                })
            },

            _validateMultiPolygonFeature: function(){
                let geojson = this.get('geojson');
                const areas = geojson.features;
                const that = this;
                if(areas !== undefined && areas.length > 0){
                    let feature = areas[0];
                    let geom = feature.geometry;
                    let geom_type = geom.type;
                    if(geom_type === 'MultiPolygon'){
                        return true;
                    }
                    else if(geom_type === "Polygon"){
                        // convert to multipolygon
                        let new_areas = areas.map(function (feature) {
                            let geom = {
                                'type': 'MultiPolygon',
                                'coordinates': [feature.geometry.coordinates]
                            };
                            feature.geometry = geom;
                            return feature;
                        });

                        let geojson = that.get('geojson');
                        geojson.features = new_areas;
                        that.set('geojson', geojson);
                        return true;
                    }
                    else {
                        return false;
                    }
                }
                return false;
            },
        
            _validateHazardClassAttribute: function () {
                const geojson = this.get('geojson');
                const areas = geojson.features;
                const that = this;
                if(areas !== undefined && areas.length > 0) {
                    let feature = areas[0];
                    return (that._geojson_attrs.hazard_class_field in feature.properties)
                }
                else {
                    return false;
                }
            }
        },
        {
            uploadHazardMap: function(hazard_map_attributes){
                return new Promise(function (resolve, reject) {
                    // Upload hazard map from file specified in HTML input dom
                    // We only handle one single GeoJSON
                    const selected_file = hazard_map_attributes.files[0]
                    const geojson = hazard_map_attributes.geojson
                    const place_name = hazard_map_attributes.place_name
                    const return_period = hazard_map_attributes.return_period
                    const hazard_model_notes = hazard_map_attributes.hazard_model_notes

                    function _process_geojson(geojson){
                        try {
                            const layer = HazardLayer.fromGeoJSON(JSON.parse(geojson));
                            layer.set({
                                place_name: place_name,
                                return_period: return_period,
                                notes: hazard_model_notes
                            })

                            // send the layer object
                            resolve(layer)

                            // Perform upload to backend in async
                            layer._createHazardMap()
                                .then(function (data) {
                                    // what to do when succeed
                                    layer.trigger('upload-finished', layer)
                                })
                                .catch(function (data) {
                                    // what to do when upload fails
                                    reject(data)
                                })
                        }
                        catch (e) {
                            reject(e)
                        }
                    }

                    if("geojson" in hazard_map_attributes){
                        _process_geojson(geojson);
                    }
                    else {

                        const reader = new FileReader()

                        reader.onload = function (e) {
                            const result = e.target.result

                            // result must be a GeoJSON
                            _process_geojson(result);
                        }

                        // Read the file as GeoJSON text
                        reader.readAsText(selected_file)
                    }
                })
            },

            fromGeoJSON: function (geojson_layer, attributes) {
                /**
                 * geojson_layer is a geojson object
                 */

                const layer = new HazardLayer(attributes)
                layer.set('geojson', geojson_layer)

                // validations
                let is_valid_geom = layer._validateMultiPolygonFeature();
                if(! is_valid_geom){
                    let e = {
                        'layer': layer,
                        'message': 'Invalid geometry types'
                    }
                    throw e
                }

                let is_valid_attributes = layer._validateHazardClassAttribute();
                if(! is_valid_attributes){

                    let e = {
                        'layer': layer,
                        'message': `Depth class attribute "${layer._geojson_attrs.hazard_class_field}" does not exists in the hazard layer`
                    }
                    throw e
                }

                const validated_geojson = layer.get('geojson');

                const areas = validated_geojson.features.map(function(value){
                    return {
                        hazard_class: value.properties[layer._geojson_attrs.hazard_class_field],
                        geometry: value.geometry
                    }
                })
                layer.set('areas', areas)
                return layer
            },
        })
    return HazardLayer
})

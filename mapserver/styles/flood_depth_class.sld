<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1.0" xmlns:se="http://www.opengis.net/se" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd">
    <NamedLayer>
        <se:Name>kartoza:flood_forecast_layer</se:Name>
        <UserStyle>
            <se:Name>kartoza:flood_forecast_layer</se:Name>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>Class 1: 0 - 0.7m</se:Name>
                    <se:Description>
                        <se:Title>Class 1: 0 - 0.7m</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>depth_class</ogc:PropertyName>
                            <ogc:Literal>1</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#f5fbff</se:SvgParameter>
                            <se:SvgParameter name="fill-opacity">0.5</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-opacity">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Class 2: 0.7 - 1.5m</se:Name>
                    <se:Description>
                        <se:Title>Class 2: 0.7 - 1.5m</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>depth_class</ogc:PropertyName>
                            <ogc:Literal>2</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#bfddf1</se:SvgParameter>
                            <se:SvgParameter name="fill-opacity">0.5</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-opacity">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Class 3: 1.5 - 3.0m</se:Name>
                    <se:Description>
                        <se:Title>Class 3: 1.5 - 3.0m</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>depth_class</ogc:PropertyName>
                            <ogc:Literal>3</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#52b4d9</se:SvgParameter>
                            <se:SvgParameter name="fill-opacity">0.5</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-opacity">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Class 4: 3.0 or greater</se:Name>
                    <se:Description>
                        <se:Title>Class 4: 3.0 or greater</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>depth_class</ogc:PropertyName>
                            <ogc:Literal>4</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#007aba</se:SvgParameter>
                            <se:SvgParameter name="fill-opacity">0.5</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-opacity">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>all other values</se:Name>
                    <se:Description>
                        <se:Title>all other values</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:Not>
                            <ogc:Or>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>depth_class</ogc:PropertyName>
                                    <ogc:Literal>1</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>depth_class</ogc:PropertyName>
                                    <ogc:Literal>2</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>depth_class</ogc:PropertyName>
                                    <ogc:Literal>3</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>depth_class</ogc:PropertyName>
                                    <ogc:Literal>4</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                            </ogc:Or>
                        </ogc:Not>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#00336c</se:SvgParameter>
                            <se:SvgParameter name="fill-opacity">0.5</se:SvgParameter>
                        </se:Fill>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#232323</se:SvgParameter>
                            <se:SvgParameter name="stroke-opacity">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

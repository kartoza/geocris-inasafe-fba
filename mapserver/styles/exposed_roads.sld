<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ogc="http://www.opengis.net/ogc" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" version="1.1.0" xmlns:se="http://www.opengis.net/se" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <se:Name>roads</se:Name>
        <UserStyle>
            <se:Name>roads</se:Name>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>Exposed Roads (Vulnerability Score)</se:Name>
                    <se:Description>
                        <se:Title>Exposed Roads (Vulnerability Score)</se:Title>
                    </se:Description>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#4a98e1</se:SvgParameter>
                            <se:SvgParameter name="stroke-opacity">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">0</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Low - hazard level >= 2</se:Name>
                    <se:Description>
                        <se:Title>Low - hazard level >= 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>depth_class</ogc:PropertyName>
                                <ogc:Literal>2</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                <ogc:Literal>0.3</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ff0820</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">2.5</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#c9fbc6</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.72</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Low - hazard level  &lt; 2</se:Name>
                    <se:Description>
                        <se:Title>Low - hazard level  &lt; 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>depth_class</ogc:PropertyName>
                                <ogc:Literal>2</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                <ogc:Literal>0.3</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#c9fbc6</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.72</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Medium - hazard level >= 2</se:Name>
                    <se:Description>
                        <se:Title>Medium - hazard level >= 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:And>
                                <ogc:PropertyIsGreaterThanOrEqualTo>
                                    <ogc:PropertyName>depth_class</ogc:PropertyName>
                                    <ogc:Literal>2</ogc:Literal>
                                </ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyIsGreaterThan>
                                    <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                    <ogc:Literal>0.3</ogc:Literal>
                                </ogc:PropertyIsGreaterThan>
                            </ogc:And>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                <ogc:Literal>0.6</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ff0000</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">2.5</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#f8ca34</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.72</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Medium - hazard level  &lt; 2</se:Name>
                    <se:Description>
                        <se:Title>Medium - hazard level  &lt; 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:And>
                                <ogc:PropertyIsLessThan>
                                    <ogc:PropertyName>depth_class</ogc:PropertyName>
                                    <ogc:Literal>2</ogc:Literal>
                                </ogc:PropertyIsLessThan>
                                <ogc:PropertyIsGreaterThan>
                                    <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                    <ogc:Literal>0.3</ogc:Literal>
                                </ogc:PropertyIsGreaterThan>
                            </ogc:And>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                <ogc:Literal>0.6</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#f8ca34</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.72</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>High - hazard level >= 2</se:Name>
                    <se:Description>
                        <se:Title>High - hazard level >= 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>depth_class</ogc:PropertyName>
                                <ogc:Literal>2</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsGreaterThan>
                                <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                <ogc:Literal>0.6</ogc:Literal>
                            </ogc:PropertyIsGreaterThan>
                        </ogc:And>
                    </ogc:Filter>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ff0000</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">2.5</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e53123</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.72</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>High - hazard level  &lt; 2</se:Name>
                    <se:Description>
                        <se:Title>High - hazard level  &lt; 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>depth_class</ogc:PropertyName>
                                <ogc:Literal>2</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                            <ogc:PropertyIsGreaterThan>
                                <ogc:PropertyName>total_vulnerability</ogc:PropertyName>
                                <ogc:Literal>0.6</ogc:Literal>
                            </ogc:PropertyIsGreaterThan>
                        </ogc:And>
                    </ogc:Filter>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#e53123</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1.72</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:se="http://www.opengis.net/se" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd">
    <NamedLayer>
        <se:Name>admin</se:Name>
        <UserStyle>
            <se:Name>admin</se:Name>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>Admin level 2</se:Name>
                    <se:Description>
                        <se:Title>Admin level 2</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>admin_level</ogc:PropertyName>
                            <ogc:Literal>2</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#001c22</se:SvgParameter>
                        </se:Fill>

                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Admin level 4</se:Name>
                    <se:Description>
                        <se:Title>Admin level 4</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>admin_level</ogc:PropertyName>
                            <ogc:Literal>4</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:PolygonSymbolizer>

                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ffffff</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Admin level 5</se:Name>
                    <se:Description>
                        <se:Title>Admin level 5</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>admin_level</ogc:PropertyName>
                            <ogc:Literal>5</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>2500000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>

                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ffffff</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Admin level 6</se:Name>
                    <se:Description>
                        <se:Title>Admin level 6</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>admin_level</ogc:PropertyName>
                            <ogc:Literal>6</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>1000000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>

                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ffffff</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Admin level bigger than 7</se:Name>
                    <se:Description>
                        <se:Title>Admin level bigger than 7</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:And>
                                <ogc:PropertyIsGreaterThanOrEqualTo>
                                    <ogc:PropertyName>admin_level</ogc:PropertyName>
                                    <ogc:Literal>7</ogc:Literal>
                                </ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyIsNull>
                                    <ogc:PropertyName>admin_level</ogc:PropertyName>
                                </ogc:PropertyIsNull>
                            </ogc:And>
                            <ogc:PropertyIsEqualTo>
                                <ogc:PropertyName>admin_level</ogc:PropertyName>
                                <ogc:Literal>1</ogc:Literal>
                            </ogc:PropertyIsEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>500000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>

                        <se:Stroke>
                            <se:SvgParameter name="stroke">#ffffff</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                        </se:Stroke>
                    </se:PolygonSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

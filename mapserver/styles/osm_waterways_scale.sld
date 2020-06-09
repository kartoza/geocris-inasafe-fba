<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:se="http://www.opengis.net/se">
    <NamedLayer>
        <se:Name>osm_waterways</se:Name>
        <UserStyle>
            <se:Name>osm_waterways</se:Name>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>canal</se:Name>
                    <se:Description>
                        <se:Title>canal</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>waterway</ogc:PropertyName>
                            <ogc:Literal>canal</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>250000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#271de7</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">2</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>ditch</se:Name>
                    <se:Description>
                        <se:Title>ditch</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>waterway</ogc:PropertyName>
                            <ogc:Literal>ditch</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>100000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#c868b3</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>drain</se:Name>
                    <se:Description>
                        <se:Title>drain</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>waterway</ogc:PropertyName>
                            <ogc:Literal>drain</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>80000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#da453b</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>river</se:Name>
                    <se:Description>
                        <se:Title>river</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:PropertyIsEqualTo>
                                <ogc:PropertyName>waterway</ogc:PropertyName>
                                <ogc:Literal>river</ogc:Literal>
                            </ogc:PropertyIsEqualTo>
                            <ogc:Not>
                                <ogc:PropertyIsNull>
                                    <ogc:PropertyName>name</ogc:PropertyName>
                                </ogc:PropertyIsNull>
                            </ogc:Not>
                        </ogc:And>
                    </ogc:Filter>

                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#487bb6</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>riverbank</se:Name>
                    <se:Description>
                        <se:Title>riverbank</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>waterway</ogc:PropertyName>
                            <ogc:Literal>riverbank</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>250000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#a276ee</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>stream</se:Name>
                    <se:Description>
                        <se:Title>stream</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>waterway</ogc:PropertyName>
                            <ogc:Literal>stream</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>250000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#d4cb41</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>Other classes</se:Name>
                    <se:Description>
                        <se:Title>Other classes</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:Not>
                            <ogc:Or>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>waterway</ogc:PropertyName>
                                    <ogc:Literal>canal</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>waterway</ogc:PropertyName>
                                    <ogc:Literal>ditch</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>waterway</ogc:PropertyName>
                                    <ogc:Literal>drain</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>waterway</ogc:PropertyName>
                                    <ogc:Literal>river</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>waterway</ogc:PropertyName>
                                    <ogc:Literal>stream</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                                <ogc:PropertyIsEqualTo>
                                    <ogc:PropertyName>waterway</ogc:PropertyName>
                                    <ogc:Literal>riverbank</ogc:Literal>
                                </ogc:PropertyIsEqualTo>
                            </ogc:Or>
                        </ogc:Not>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>100000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#53ecb7</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">4</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">round</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">round</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>river</se:Name>
                    <se:Description>
                        <se:Title>river</se:Title>
                    </se:Description>
                    <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
                        <ogc:And>
                            <ogc:PropertyIsEqualTo>
                                <ogc:PropertyName>waterway</ogc:PropertyName>
                                <ogc:Literal>river</ogc:Literal>
                            </ogc:PropertyIsEqualTo>
                            <ogc:PropertyIsNull>
                                <ogc:PropertyName>name</ogc:PropertyName>
                            </ogc:PropertyIsNull>
                        </ogc:And>
                    </ogc:Filter>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>250000</se:MaxScaleDenominator>
                    <se:LineSymbolizer>
                        <se:Stroke>
                            <se:SvgParameter name="stroke">#487bb6</se:SvgParameter>
                            <se:SvgParameter name="stroke-width">1</se:SvgParameter>
                            <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
                            <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
                        </se:Stroke>
                    </se:LineSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

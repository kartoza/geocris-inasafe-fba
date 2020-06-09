<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" version="1.1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:se="http://www.opengis.net/se" xmlns:ogc="http://www.opengis.net/ogc" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <NamedLayer>
        <se:Name>osm_buildings</se:Name>
        <UserStyle>
            <se:Name>osm_buildings</se:Name>
            <se:FeatureTypeStyle>
                <se:Rule>
                    <se:Name>All Buildings As Polys</se:Name>
                    <se:Description>
                        <se:Title>Buildings</se:Title>
                    </se:Description>
                    <se:MinScaleDenominator>1</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>10000</se:MaxScaleDenominator>
                    <se:PolygonSymbolizer>
                        <se:Fill>
                            <se:SvgParameter name="fill">#ffffff</se:SvgParameter>
                        </se:Fill>
                    </se:PolygonSymbolizer>
                </se:Rule>
                <se:Rule>
                    <se:Name>All buildings</se:Name>
                    <se:Description>
                        <se:Title>OSM Buildings</se:Title>
                    </se:Description>
                    <se:MinScaleDenominator>10001</se:MinScaleDenominator>
                    <se:MaxScaleDenominator>25000</se:MaxScaleDenominator>
                    <se:PointSymbolizer>
                        <se:Graphic>
                            <se:Mark>
                                <se:WellKnownName>square</se:WellKnownName>
                                <se:Fill>
                                    <se:SvgParameter name="fill">#ffffff</se:SvgParameter>
                                </se:Fill>

                            </se:Mark>
                            <se:Size>7</se:Size>
                        </se:Graphic>
                    </se:PointSymbolizer>
                </se:Rule>
            </se:FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>

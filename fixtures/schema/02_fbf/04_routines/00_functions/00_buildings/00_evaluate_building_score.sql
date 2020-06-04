
CREATE OR REPLACE FUNCTION public.kartoza_evaluate_building_score() RETURNS VARCHAR
    LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE osm_buildings
    SET building_area = st_area(public.osm_buildings.geometry::geography)
    WHERE building_area is null;
    UPDATE osm_buildings
    SET building_area_score = CASE
                                  WHEN building_area <= 10 THEN 1
                                  WHEN building_area > 10 and building_area <= 30 THEN 0.7
                                  WHEN building_area > 30 and building_area <= 100 THEN 0.5
                                  WHEN building_area > 100 THEN 0.3
                                  ELSE 0.3
    END
    WHERE building_area_score is null;
    UPDATE osm_buildings
    SET building_material_score =
            CASE
                WHEN "building:material" ILIKE 'brick%' THEN 0.5
                WHEN "building:material" = 'concrete' THEN 0.1
                ELSE 0.3
                END
    WHERE building_material_score is null;
    UPDATE osm_buildings
    SET building_type = CASE
                            WHEN amenity ILIKE '%school%' OR amenity ILIKE '%kindergarten%' THEN 'School'
                            WHEN amenity ILIKE '%university%' OR amenity ILIKE '%college%' THEN 'University/College'
                            WHEN amenity ILIKE '%government%' THEN 'Government'
                            WHEN amenity ILIKE '%clinic%' OR amenity ILIKE '%doctor%' THEN 'Clinic/Doctor'
                            WHEN amenity ILIKE '%hospital%' THEN 'Hospital'
                            WHEN amenity ILIKE '%fire%' THEN 'Fire Station'
                            WHEN amenity ILIKE '%police%' THEN 'Police Station'
                            WHEN amenity ILIKE '%public building%' THEN 'Public Building'
                            WHEN amenity ILIKE '%worship%' and (religion ILIKE '%islam' or religion ILIKE '%muslim%')
                                THEN 'Place of Worship - Islam'
                            WHEN amenity ILIKE '%worship%' and religion ILIKE '%budd%' THEN 'Place of Worship - Buddhist'
                            WHEN amenity ILIKE '%worship%' and religion ILIKE '%unitarian%' THEN 'Place of Worship - Unitarian'
                            WHEN amenity ILIKE '%mall%' OR amenity ILIKE '%market%' THEN 'Supermarket'
                            WHEN landuse ILIKE '%residential%' OR use = 'residential' THEN 'Residential'
                            WHEN landuse ILIKE '%recreation_ground%' OR leisure IS NOT NULL AND leisure != '' THEN 'Sports Facility'
        -- run near the end
                            WHEN amenity = 'yes' THEN 'Residential'
                            WHEN use = 'government' AND "type" IS NULL THEN 'Government'
                            WHEN use = 'residential' AND "type" IS NULL THEN 'Residential'
                            WHEN use = 'education' AND "type" IS NULL THEN 'School'
                            WHEN use = 'medical' AND "type" IS NULL THEN 'Clinic/Doctor'
                            WHEN use = 'place_of_worship' AND "type" IS NULL THEN 'Place of Worship'
                            WHEN use = 'school' AND "type" IS NULL THEN 'School'
                            WHEN use = 'hospital' AND "type" IS NULL THEN 'Hospital'
                            WHEN use = 'commercial' AND "type" IS NULL THEN 'Commercial'
                            WHEN use = 'industrial' AND "type" IS NULL THEN 'Industrial'
                            WHEN use = 'utility' AND "type" IS NULL THEN 'Utility'
        -- Add default type
                            WHEN "type" IS NULL THEN 'Residential'
        END
    WHERE building_type is null;
    UPDATE osm_buildings
    SET building_type_score =
            CASE
                WHEN building_type = 'Clinic/Doctor' THEN 0.7
                WHEN building_type = 'Commercial' THEN 0.7
                WHEN building_type = 'School' THEN 1
                WHEN building_type = 'Government' THEN 0.7
                WHEN building_type ILIKE 'Place of Worship%' THEN 0.5
                WHEN building_type = 'Residential' THEN 1
                WHEN building_type = 'Police Station' THEN 0.7
                WHEN building_type = 'Fire Station' THEN 0.7
                WHEN building_type = 'Hospital' THEN 0.7
                WHEN building_type = 'Supermarket' THEN 0.7
                WHEN building_type = 'Sports Facility' THEN 0.3
                WHEN building_type = 'University/College' THEN 1.0
                ELSE 0.3
                END
    WHERE building_type_score is null;
    UPDATE osm_buildings
    SET total_vulnerability = (building_area_score + building_material_score + building_type_score) / 3
    WHERE total_vulnerability is null;
    RETURN 'OK';
END
$$;

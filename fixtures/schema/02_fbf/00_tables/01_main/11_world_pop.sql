create table if not exists world_pop
(
    rid      serial not null
        constraint world_pop_pkey
            primary key,
    rast     raster
        constraint enforce_nodata_values_rast
            check (_raster_constraint_nodata_values(rast) =
                   '{-99999.0000000000}'::numeric[])
        constraint enforce_out_db_rast
            check (_raster_constraint_out_db(rast) = '{f}'::boolean[])
        constraint enforce_pixel_types_rast
            check (_raster_constraint_pixel_types(rast) = '{32BF}'::text[])
        constraint enforce_scalex_rast
            check (round((st_scalex(rast))::numeric, 10) =
                   round(0.000833333330002896, 10))
        constraint enforce_scaley_rast
            check (round((st_scaley(rast))::numeric, 10) =
                   round((- 0.000833333330000975), 10))
        constraint enforce_num_bands_rast
            check (st_numbands(rast) = 1)
        constraint enforce_same_alignment_rast
            check (st_samealignment(rast,
                                    '0100000000A96313B3814E4B3F751E13B3814E4BBF891DD0F08BC357406F26E36EC94F184000000000000000000000000000000000E610000001000100'::raster))
        constraint enforce_srid_rast
            check (st_srid(rast) = 4326),
    filename text
);

create index if not exists world_pop_st_convexhull_idx
    on world_pop (st_convexhull(rast));

create sequence if not exists world_pop_rid_seq;

alter sequence world_pop_rid_seq owned by world_pop.rid;

ALTER TABLE ONLY world_pop ALTER COLUMN rid SET DEFAULT nextval('public.world_pop_rid_seq'::regclass);

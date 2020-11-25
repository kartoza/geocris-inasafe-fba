create table if not exists building_global_key_mapping (
    id bigint not null,
    id_mapping bigint,
    key character varying,
    constraint building_global_key_mapping_pkey primary key (id_mapping, key)
);

create sequence if not exists building_global_key_mapping_seq
    as bigint
    start with 1
    increment by 1
    no minvalue
    no maxvalue
    cache 1;

alter sequence building_global_key_mapping_seq owned by building_global_key_mapping.id;

alter table only building_global_key_mapping alter column id set default nextval('building_global_key_mapping_seq'::regclass);

create table if not exists admin_boundary_global_key_mapping (
    id bigint not null,
    id_mapping bigint,
    key character varying,
    partition character varying,
    partition_level int,
    constraint admin_boundary_global_key_mapping_pkey primary key (id_mapping, key)
);

create sequence if not exists admin_boundary_global_key_mapping_seq
    as bigint
    start with 1
    increment by 1
    no minvalue
    no maxvalue
    cache 1;

alter sequence admin_boundary_global_key_mapping_seq owned by admin_boundary_global_key_mapping.id;

alter table only admin_boundary_global_key_mapping alter column id set default nextval('admin_boundary_global_key_mapping_seq'::regclass);

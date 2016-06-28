create table fdfs_info(
    id int NOT NULL AUTO_INCREMENT,
    file_name varchar(100),
    file_size integer,
    file_md5 varchar(32),
    file_crc32 varchar(10),
    file_group varchar(8),
    file_local_path varchar(100),
    domain_name varchar(32),
    PRIMARY KEY(id)
);
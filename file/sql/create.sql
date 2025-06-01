CREATE DATABASE aitaSystem
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

use aitaSystem;


-- 用户表
create table if not exists user
(
    id           bigint auto_increment comment 'id' primary key,
    userAccount  varchar(256)                           not null comment '账号',
    userPassword varchar(512)                           not null comment '密码',
    userName     varchar(256)                           null comment '用户昵称',
    userAvatar   varchar(1024)                          null comment '用户头像',
    userProfile  varchar(512)                           null comment '用户简介',
    userRole     varchar(256) default 'user'            not null comment '用户角色：user/admin/ban',
    isDelete     tinyint      default 0                 not null comment '是否删除'
    ) comment '用户';




create table data
(
    data_id         int auto_increment
        primary key,
    data_title      varchar(200) null,
    data_content    text         null,
    data_date       datetime     null,
    data_author     varchar(50)  null,
    data_link       varchar(255) null,
    data_read_count int          null,
    data_image_url  text         null,
    data_type       varchar(30)  null,
    data_abstract   text         null
);

create table data_label
(
    label_id          int auto_increment
        primary key,
    label_name        varchar(30) null,
    label_description text        null
);

create table `group`
(
    group_id                 int auto_increment
        primary key,
    group_type               varchar(20) null,
    group_role               varchar(20) null,
    group_person_name        varchar(20) null,
    group_person_description varchar(20) null,
    group_person_image_url   text        null,
    group_person_content     text        null,
    group_person_papers      text        null
);

create table hxxm
(
    id              int auto_increment
        primary key,
    name            varchar(255) null,
    description     text         null,
    client          varchar(255) null,
    start_date      datetime     null,
    end_date        datetime     null,
    project_manager varchar(100) null,
    budget          float        null
);

create table models
(
    models_id         int auto_increment
        primary key,
    models_disease    varchar(255) null,
    models_name       varchar(255) null,
    models_input_type varchar(255) null,
    models_input_num  int          null,
    models_path       varchar(255) null,
    models_parameters varchar(255) null
);

create table news
(
    news_id         int auto_increment
        primary key,
    news_title      varchar(100) null,
    news_content    text         null,
    news_author     varchar(20)  null,
    news_date       datetime     null,
    news_link       varchar(100) null,
    news_read_count int          null,
    news_image_url  text         null,
    label_id        int          null
);

create table news_label
(
    label_id          int auto_increment
        primary key,
    label_name        varchar(20) null,
    label_description text        null
);

create table papers
(
    id          int auto_increment
        primary key,
    title       varchar(200) null,
    content     text         null,
    create_time datetime     null,
    author      varchar(100) null,
    image_url   varchar(255) null,
    abstract    text         null,
    keywords    varchar(255) null
);

create table software
(
    software_id     int auto_increment
        primary key,
    software_belong varchar(255) null,
    software_type   varchar(255) null,
    software_url    varchar(255) null
);

create table zxxm
(
    id                     int auto_increment
        primary key,
    name                   varchar(255) null,
    description            text         null,
    funding_agency         varchar(255) null,
    start_date             datetime     null,
    end_date               datetime     null,
    principal_investigator varchar(100) null,
    budget                 float        null,
    status                 varchar(50)  null
);





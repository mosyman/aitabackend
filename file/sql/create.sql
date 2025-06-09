# 建表sql脚本
CREATE DATABASE aitaSystem
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

use aitasystem;


-- 用户表
create table if not exists user
(
    id           bigint auto_increment comment 'id' primary key,
    account  varchar(256)                           not null comment '账号',
    password varchar(512)                           not null comment '密码',
    name     varchar(256)                           null comment '用户昵称',
    avatar   varchar(1024)                          null comment '用户头像',
    profile  varchar(512)                           null comment '用户简介',
    role     varchar(256) default 'user'            not null comment '用户角色：user/admin/ban',
    reviewStatus  tinyint  default 0                 not null comment '审核状态：0-待审核，1-通过，2-拒绝',
    isDelete     tinyint      default 0                 not null comment '0不删除，1删除'
    ) comment '用户';




-- 数据集
CREATE TABLE dataset (
     id                  BIGINT AUTO_INCREMENT COMMENT 'ID' PRIMARY KEY,
     title               VARCHAR(256) NULL COMMENT '标题',
     content             TEXT NULL COMMENT '内容',
     author              VARCHAR(128) NULL COMMENT '作者',
     link                VARCHAR(1024) NULL COMMENT '链接',
     image_url           VARCHAR(1024) NULL COMMENT '图片URL',
     type                VARCHAR(128) NULL COMMENT '类型',
     abstract          TEXT NULL COMMENT '摘要',
     createTime         DATETIME DEFAULT CURRENT_TIMESTAMP NULL COMMENT '创建时间',
     updateTime         DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NULL COMMENT '修改时间',
     isDelete          TINYINT DEFAULT 0 NOT NULL COMMENT '是否删除'
) COMMENT='数据集表';

-- 论文表
CREATE TABLE IF NOT EXISTS papers (
  id BIGINT UNSIGNED AUTO_INCREMENT COMMENT '论文ID' PRIMARY KEY,
  title VARCHAR(255) NOT NULL COMMENT '论文标题',
  content text COMMENT '论文正文',
  publishTime DATETIME NULL COMMENT '发布时间',
  author VARCHAR(100) NOT NULL COMMENT '作者',
  abstract TEXT COMMENT '摘要',
  keywords VARCHAR(500) COMMENT '关键词，逗号分隔',
  citation_count INT UNSIGNED DEFAULT 0 COMMENT '被引用次数',
  source VARCHAR(100) COMMENT '论文来源',
  doi VARCHAR(100) COMMENT 'DOI编号',
  pdf_url VARCHAR(2083) COMMENT 'PDF文件URL',
  createTime   datetime     default CURRENT_TIMESTAMP not null comment '创建时间',
  updateTime   datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
  isDelete TINYINT DEFAULT 0 NOT NULL COMMENT '是否删除'
)  COMMENT='论文表';


-- 团队成员表
CREATE TABLE team_members (
      id INT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(50) NOT NULL COMMENT '姓名',
      gender tinyint default 0 COMMENT '性别0-男 1-女',
      ethnicity VARCHAR(30) COMMENT '民族',
      department VARCHAR(100) COMMENT '系所',
      position VARCHAR(50) COMMENT '职务',
      title VARCHAR(50) COMMENT '职称',
      phone VARCHAR(20) COMMENT '办公电话',
      email VARCHAR(100) UNIQUE COMMENT '电子邮箱',
      image_url VARCHAR(255) COMMENT '照片',
      profile TEXT COMMENT '个人简介',
      areas TEXT COMMENT '研究领域',
      courses TEXT COMMENT '主讲课程',
      patents TEXT COMMENT '专利',
      projects TEXT COMMENT '科研项目',
      publications TEXT COMMENT '论文',
      honors TEXT COMMENT '荣誉',
      isDelete TINYINT DEFAULT 0 NOT NULL COMMENT '是否删除'
)  COMMENT='团队成员表';



CREATE TABLE news (
      id BIGINT AUTO_INCREMENT COMMENT '新闻ID' PRIMARY KEY,
      title VARCHAR(128) NOT NULL COMMENT '新闻标题',
      content TEXT NOT NULL COMMENT '新闻内容',
      author VARCHAR(128) DEFAULT '佚名' COMMENT '作者名称',
      publish_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
      link VARCHAR(256) COMMENT '原文链接',
      image_url TEXT COMMENT '封面图URL',
      isDelete TINYINT DEFAULT 0 NOT NULL COMMENT '删除标志：0-正常，1-已删除',
      createTime   datetime     default CURRENT_TIMESTAMP not null comment '创建时间',
      updateTime   datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间'
) COMMENT='新闻表';





-- 项目表
CREATE TABLE IF NOT EXISTS project (
   id BIGINT AUTO_INCREMENT COMMENT 'id' PRIMARY KEY,
   type TINYINT NOT NULL COMMENT '项目类型：1=hxxm(横向项目), 2=zxxm(纵向项目)',

-- 公共字段
   name VARCHAR(255) NULL COMMENT '项目名称',
   description TEXT NULL COMMENT '项目描述',
   start_date DATETIME NULL COMMENT '开始日期',
   end_date DATETIME NULL COMMENT '结束日期',
   budget FLOAT NULL COMMENT '预算金额',
   isDelete TINYINT DEFAULT 0 NOT NULL COMMENT '是否删除',

-- hxxm 特有字段
   client VARCHAR(255) NULL COMMENT '客户名称',
   project_manager VARCHAR(100) NULL COMMENT '项目经理',

-- zxxm 特有字段
   funding_agency VARCHAR(255) NULL COMMENT '资助机构',
   principal_investigator VARCHAR(100) NULL COMMENT '项目负责人',
   status VARCHAR(50) NULL COMMENT '项目状态',
   createTime   datetime     default CURRENT_TIMESTAMP not null comment '创建时间',
   updateTime   datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间'
);
CREATE TABLE IF NOT EXISTS `user` (
	`id` BIGINT AUTO_INCREMENT UNIQUE COMMENT '主键',
	`username` VARCHAR(255) COMMENT '用户名',
	`password` VARCHAR(255) COMMENT '密码',
	`phone` VARCHAR(255) UNIQUE COMMENT '手机号',
	`refresh_token` VARCHAR(255) COMMENT '长token',
	`token_expiration_time` BIGINT COMMENT 'token过期时间',
	`registration` BIGINT NOT NULL DEFAULT 0 COMMENT '注册时间',
	`enable` BOOLEAN NOT NULL DEFAULT false COMMENT '是否禁用 true : 可用  false：不可用',
	`last_login_time` TIMESTAMP COMMENT '最后登录时间',
	PRIMARY KEY(`id`)
) COMMENT='用户表';


CREATE TABLE IF NOT EXISTS `account` (
	`id` BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` VARCHAR(255) COMMENT '账户名',
	`balance` DECIMAL(10,2) COMMENT '账单余额',
	`user_id` BIGINT COMMENT '用户id',
	PRIMARY KEY(`id`)
) COMMENT='账户表';


CREATE TABLE IF NOT EXISTS `income` (
	`id` BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	`money` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '金额',
	`account_id` BIGINT NOT NULL DEFAULT 0 COMMENT '账户id',
	`user_id` BIGINT NOT NULL DEFAULT 0 COMMENT '人员id',
	`remark` VARCHAR(255) COMMENT '备注',
	`income_time` TIMESTAMP COMMENT '收入时间',
	`create_time` TIMESTAMP COMMENT '创建时间',
	`enable` BOOLEAN NOT NULL DEFAULT true COMMENT '是否可用',
	`income_type_id` BIGINT COMMENT '消费类型id',
	PRIMARY KEY(`id`)
) COMMENT='收入表';


CREATE TABLE IF NOT EXISTS `expend` (
	`id` BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	`money` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '金额',
	`account_id` BIGINT NOT NULL DEFAULT 0 COMMENT '账户id',
	`user_id` BIGINT NOT NULL DEFAULT 0 COMMENT '人员id',
	`remark` VARCHAR(255) COMMENT '备注',
	`expend_time` TIMESTAMP COMMENT '支出时间',
	`create_time` TIMESTAMP COMMENT '创建时间',
	`enable` BOOLEAN NOT NULL DEFAULT true COMMENT '是否可用',
	`consumption_id` BIGINT COMMENT '消费类型id',
	PRIMARY KEY(`id`)
) COMMENT='支出表';

CREATE TABLE IF NOT EXISTS `expend_type` (
	`id` BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	`expend_type_name` VARCHAR(255) COMMENT '消费类型说明',
	`enable` BOOLEAN NOT NULL COMMENT '是否禁用 true : 可用  false：不可用',
	`create_time` TIMESTAMP NOT NULL,
	PRIMARY KEY(`id`)
) COMMENT='消费类型表';


CREATE TABLE IF NOT EXISTS `income_type` (
	`id` BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	`income_type_name` VARCHAR(255) COMMENT '收入类型名称',
	`create_time` TIMESTAMP NOT NULL COMMENT '创时间',
	`enable` BOOLEAN NOT NULL DEFAULT true COMMENT '是否可用',
	PRIMARY KEY(`id`)
) COMMENT='收入类型表';


CREATE TABLE IF NOT EXISTS `config_version` (
	`id` BIGINT NOT NULL AUTO_INCREMENT UNIQUE,
	`expend_type_version` BIGINT NOT NULL COMMENT '支出类型版本',
	`income_type_version` BIGINT NOT NULL COMMENT '收入类型版本',
	`account_version` BIGINT NOT NULL COMMENT '账户表版本',
	PRIMARY KEY(`id`)
);


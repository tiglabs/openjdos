CREATE DATABASE sunshine_dashboard
  DEFAULT CHARACTER SET utf8
  COLLATE utf8_general_ci;

use sunshine_dashboard;
CREATE TABLE `envs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `env_id` VARCHAR(64) NOT NULL COMMENT '环境id',
  `env_name` varchar(64) NOT NULL COMMENT '环境名称',
  `env_desc` varchar(128) NOT NULL COMMENT '环境描述',
  `deploy_type` varchar(32) NOT NULL COMMENT '部署类型',
  `owner` varchar(64) NOT NULL COMMENT '用户',
  `status` VARCHAR(32) NOT NULL COMMENT '状态',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='环境部署表';

CREATE TABLE `envs_host` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `env_id` VARCHAR(64) NOT NULL COMMENT '环境id',
  `host_ip` varchar(128) NOT NULL COMMENT '主机IP',
  `host_type` varchar(32) NOT NULL COMMENT '主机类型（master,node,etcd,net）',
  `working_status` varchar(32) NOT NULL COMMENT '当前主机是否提供服务',
  `status` VARCHAR(32) NOT NULL COMMENT '服务状态',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='环境部署主机表';

CREATE TABLE `envs_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `env_id` VARCHAR(64) NOT NULL COMMENT '环境id',
  `operate_type` varchar(64) NOT NULL COMMENT '操作类型',
  `operate_owner` varchar(64) NOT NULL COMMENT '操作人',
  `operate_desc` varchar(256) COMMENT '操作描述',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='环境部署操作表';
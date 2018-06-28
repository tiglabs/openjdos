
DROP DATABASE IF EXISTS sunshine;

CREATE DATABASE sunshine DEFAULT CHARACTER SET utf8;

use sunshine;

DROP TABLE IF EXISTS  `sunshine`.`user`;
CREATE TABLE  `sunshine`.`user` (
  `uuid` varchar(32) NOT NULL UNIQUE,
  `name` varchar(128) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `salt` varchar(128) DEFAULT NULL,
  `locked` boolean DEFAULT FALSE ,
  `lastOpDate` timestamp ON UPDATE CURRENT_TIMESTAMP COMMENT 'last operation date',
  `createDate` timestamp,
  PRIMARY KEY  (`uuid`),
  CONSTRAINT `uqUser` UNIQUE(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS  `sunshine`.`role`;
CREATE TABLE  `sunshine`.`role` (
  `uuid` varchar(32) NOT NULL UNIQUE,
  `role` varchar(128) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `lastOpDate` timestamp ON UPDATE CURRENT_TIMESTAMP COMMENT 'last operation date',
  `createDate` timestamp,
  PRIMARY KEY  (`uuid`),
  CONSTRAINT `uqRole` UNIQUE(`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS  `sunshine`.`permission`;
CREATE TABLE  `sunshine`.`permission` (
  `uuid` varchar(32) NOT NULL UNIQUE,
  `name` varchar(128) NOT NULL,
  `type` varchar(64) NOT NULL,
  `permission` varchar(255) DEFAULT NULL,
  `lastOpDate` timestamp ON UPDATE CURRENT_TIMESTAMP COMMENT 'last operation date',
  `createDate` timestamp,
  PRIMARY KEY  (`uuid`),
  CONSTRAINT `uqPermission` UNIQUE(`permission`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS  `sunshine`.`user_role_ref`;
CREATE TABLE  `sunshine`.`user_role_ref` (
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT,
  `userUuid` varchar(32) NOT NULL,
  `roleUuid` varchar(32) NOT NULL,
  `lastOpDate` timestamp ON UPDATE CURRENT_TIMESTAMP COMMENT 'last operation date',
  `createDate` timestamp,
  PRIMARY KEY  (`id`),
  CONSTRAINT `fkUserRoleRefUserUuid` FOREIGN KEY (`userUuid`) REFERENCES `user` (`uuid`) ON DELETE CASCADE,
  CONSTRAINT `fkUserRoleRefRoleUuid` FOREIGN KEY (`roleUuid`) REFERENCES `role` (`uuid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS  `sunshine`.`role_permission_ref`;
CREATE TABLE  `sunshine`.`role_permission_ref` (
  `id` bigint unsigned NOT NULL UNIQUE AUTO_INCREMENT,
  `roleUuid` varchar(32) NOT NULL,
  `permissionUuid` varchar(32) NOT NULL,
  `lastOpDate` timestamp ON UPDATE CURRENT_TIMESTAMP COMMENT 'last operation date',
  `createDate` timestamp,
  PRIMARY KEY  (`id`),
  CONSTRAINT `fkRolePermissionRefRoleUuid` FOREIGN KEY (`roleUuid`) REFERENCES `role` (`uuid`) ON DELETE CASCADE,
  CONSTRAINT `fkRolePermissionRefPermissionUuid` FOREIGN KEY (`permissionUuid`) REFERENCES `permission` (`uuid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `user`(uuid, name, password, salt, locked, lastOpDate, createDate)
    VALUES ('33d82c666e1d11e89f250026551ab510','admin','admin','',FALSE ,NULL ,NOW()),
      ('8aad10746e1d11e89f250026551ab510','user','user','',FALSE ,NULL ,NOW());

INSERT INTO `role`(uuid, role, description, lastOpDate, createDate)
    VALUES ('a7709c6c6e1d11e89f250026551ab510','admin','admin',NULL ,NOW()),
      ('c1d742c26e1d11e89f250026551ab510','user','user',NULL ,NOW());

INSERT INTO permission(uuid, name, type, permission, lastOpDate, createDate)
    VALUES ('dc3118006e1d11e89f250026551ab510','project','OPERATION','project:*',NULL ,NOW()),
      ('1f94fce26e1e11e89f250026551ab510','project','OPERATION','project:view',NULL ,NOW());

INSERT INTO user_role_ref(userUuid, roleUuid, lastOpDate, createDate)
    VALUES ('33d82c666e1d11e89f250026551ab510','a7709c6c6e1d11e89f250026551ab510',NULL ,NOW()),
      ('8aad10746e1d11e89f250026551ab510','c1d742c26e1d11e89f250026551ab510',NULL ,NOW());

INSERT INTO role_permission_ref(roleUuid, permissionUuid, lastOpDate, createDate)
VALUES ('a7709c6c6e1d11e89f250026551ab510','dc3118006e1d11e89f250026551ab510',NULL ,NOW()),
  ('c1d742c26e1d11e89f250026551ab510','1f94fce26e1e11e89f250026551ab510',NULL ,NOW());

-- create databases
CREATE DATABASE IF NOT EXISTS vcdb;
CREATE DATABASE IF NOT EXISTS userdb;

use vcdb;
CREATE TABLE `branch`(
    `bid` int not null AUTO_INCREMENT,
    `name` varchar(125) NOT NULL,
    `tail` varchar(500) not null,
    PRIMARY KEY (`bid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


insert into branch values ("func1", "testt1");
insert into branch values ("func2", "testt2");


CREATE TABLE `commit`(
    `version` varchar(500) not null,
    `branch` varchar(500) not null,
    `last_version` varchar(500) not null,
    `upgrade` varchar(5000) not null,
    `downgrade` varchar(5000) not null,
    `time` datetime not null,
    `msg` varchar(500) not null,
    PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `merge`(
    `mid` int not null AUTO_INCREMENT,
    `version` varchar(500) not null,
    `merge_from` varchar(500) not null,
    PRIMARY KEY (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;



CREATE TABLE `user`(
    `uid` varchar(500) not null,
    `name` varchar(125) not null,
    `email` varchar(125) not null,
    `current_version` varchar(500) not null,
    `current_branch` varchar(500) not null,
    PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

insert into user values ("testtt", "elaine", "elaine.com", "testtt1", "func1");


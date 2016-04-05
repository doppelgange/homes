create database homes;
use homes;
drop table `homes`;
CREATE TABLE `homes` (
	`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`uuid` char(36) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Homes UUID',
	`full_address` varchar(255) DEFAULT NULL,
	`latitude` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Homes latitude',
	`longitude` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Homes longitude',
	`bathrooms` int(2) unsigned DEFAULT NULL,
	`bedrooms` int(2) unsigned DEFAULT NULL,
	`car_space` int(2) unsigned DEFAULT NULL,
	`homes_ev` int(10) unsigned DEFAULT NULL COMMENT 'Homes estimated value',
	`rv`  int(10) unsigned DEFAULT NULL,
	`land_value` int(10) unsigned DEFAULT NULL,
	`improvement_value` int(10) unsigned DEFAULT NULL,
	`land_area` int(10) unsigned DEFAULT NULL,
	`floor_area` int(10)  unsigned DEFAULT NULL,
	`decade_built` int(10)  unsigned DEFAULT NULL,
	`recent_sold` tinyint(1) DEFAULT NULL,
	`remarks` text DEFAULT NULL,

	`list_date` date DEFAULT NULL COMMENT 'List date from trademe or agent site',
	`sold_date` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`sold_price` int(10)  unsigned DEFAULT NULL,
	`open2view_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`agent` varchar(255) DEFAULT NULL,
	`agent_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`agent_ref` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`headline` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`description` text DEFAULT NULL,
	`legal_desc` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`rates` decimal(8,2) DEFAULT NULL,
	`chattles` text DEFAULT NULL,
	`method` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`qv_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`trademe_url`	varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`google_street_view_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`street` varchar(255) DEFAULT NULL,
	`suburb` varchar(255) DEFAULT NULL,
	`state` varchar(255) DEFAULT NULL,
	`postcode` varchar(255) DEFAULT NULL,
	`updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

truncate homes;

CREATE TABLE `test` (
	`id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	`uuid` char(36) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Homes UUID',
	`full_address` varchar(255) DEFAULT NULL,
	`google_street_view_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
	`updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
select * from test;

INSERT INTO `test` (`uuid`, `full_address`, `google_street_view_url`)
VALUES
	( 'AAAA', 'AAAA', 'AAAA');

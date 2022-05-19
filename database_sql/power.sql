SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `func_unit`;
CREATE TABLE `func_unit`  (
  `func_unit_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '功能部件唯一的主键id',
  `func_unit_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '功能部件名称或者描述',
  `loc_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '所处服务器的IP地址',
  `server_machine_id` int(10) NOT NULL COMMENT '所属服务器的主键id',
  `func_unit_tdp` int(5) NOT NULL COMMENT '功能部件的tdp',
  `type` int(5) NOT NULL COMMENT '功能部件的类型 1：cpu 2：服务器 3：controller 4：更高级的controller',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`func_unit_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `coincidence_relation`;
CREATE TABLE `coincidence_relation`  (
  `coincidence_relation_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '对应关系的唯一主键',
  `coincidence_relation_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '对应关系名称或者描述',
  `father_id` int(10) NOT NULL COMMENT '父id（外键）',
  `son_id` int(10) NOT NULL COMMENT '子id（外键）',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`coincidence_relation_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `unit_capping`;
CREATE TABLE `unit_capping`  (
  `unit_capping_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'capping动作的唯一主键',
  `unit_capping_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT 'capping动作的名称或者描述',
  `func_unit_id` int(10) NOT NULL COMMENT '对应功能部件的id',
  `capping_value` int(5) NOT NULL COMMENT 'capping的值',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间，记录capping动作的时间',
  PRIMARY KEY (`unit_capping_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `unit_power`;
CREATE TABLE `unit_power`  (
  `unit_power_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '部件实时功耗的唯一id',
  `unit_power_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '部件实时功耗名称或者描述',
  `func_unit_id` int(10) NOT NULL COMMENT '对应功能部件的id',
  `unit_power` int(5) NOT NULL COMMENT '功能部件的功耗',
  `unit_usage` int(5) NOT NULL DEFAULT 0 COMMENT '功能部件的利用率',
  `unit_temperature` int(5) NOT NULL DEFAULT 0 COMMENT '功能部件的温度',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`unit_power_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

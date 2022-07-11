/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : controller_server

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 19/05/2022 19:50:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for capping
-- ----------------------------
DROP TABLE IF EXISTS `capping`;
CREATE TABLE `capping`  (
  `capping_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'capping记录id',
  `capping_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT 'capping名称，信息描述',
  `controller_server_id` int(10) NOT NULL COMMENT '控制器agent对应关系的主键',
  `capping_value` float(6,2) NOT NULL COMMENT 'capping的值',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间，记录capping动作的时间',
  PRIMARY KEY (`capping_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for controller
-- ----------------------------
DROP TABLE IF EXISTS `controller`;
CREATE TABLE `controller`  (
  `controller_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'controller主键id',
  `controller_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '控制器名称，信息描述',
  `server_machine_id` int(10) NOT NULL COMMENT '控制器所处的服务器id（外键）',
  `rack_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '对应的机架信息',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`controller_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for server_machine
-- ----------------------------
DROP TABLE IF EXISTS `server_machine`;
CREATE TABLE `server_machine`  (
  `server_machine_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '服务器主键id',
  `server_machine_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '服务器名称，信息描述',
  `server_machine_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '服务器ip地址',
  `server_machine_tdp` int(5) NOT NULL COMMENT '服务器的tdp的值',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`server_machine_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for server_machine_power
-- ----------------------------
DROP TABLE IF EXISTS `server_machine_power`;
CREATE TABLE `server_machine_power`  (
  `server_machine_power_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '服务器实时功耗id',
  `server_machine_power_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '服务器实时功耗名称，信息描述',
  `server_machine_id` int(10) NOT NULL COMMENT '服务器id（外键）',
  `server_machine_power` float(6,2) NOT NULL COMMENT '服务器的实时功耗的值',
  `server_machine_usage` float(6,2) NOT NULL COMMENT '服务器的利用率',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`server_machine_power_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `power_line`;
CREATE TABLE `power_line`  (
  `power_line_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '线路的唯一主键',
  `power_line_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '线路名称，信息描述',
  `power_line_tdp` int(5) NOT NULL COMMENT '线路的tdp的值',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`power_line_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;


DROP TABLE IF EXISTS `line_server`;
CREATE TABLE `line_server`  (
  `line_server_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '线路服务器供应关系id',
  `line_server_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '线路服务器供应关系名称，信息描述',
  `server_machine_id` int(10) NOT NULL COMMENT '服务器id（外键）',
  `power_line_id` int(10) NOT NULL COMMENT '线路id（外键）',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`line_server_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `line_controller`;
CREATE TABLE `line_controller`  (
  `line_controller_id` int(10) NOT NULL AUTO_INCREMENT COMMENT '线路机架供应关系id',
  `line_controller_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '线路机架供应关系名称，信息描述',
  `controller_id` int(10) NOT NULL COMMENT '控制器id（外键）',
  `power_line_id` int(10) NOT NULL COMMENT '线路id（外键）',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`line_controller_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

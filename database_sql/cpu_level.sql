/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : cpu_level

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 19/05/2022 19:50:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;



DROP TABLE IF EXISTS `cpu_capping`;
CREATE TABLE `cpu_capping`  (
  `cpu_capping_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'capping细节记录id',
  `capping_id` int(10) NOT NULL  COMMENT '服务器capping记录id',
  `cpu_capping_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT 'capping名称，信息描述',
  `cpu_id` int(10) NOT NULL COMMENT '对应cpu的id',
  `cpu_power` float(6,2) NOT NULL COMMENT 'cpu的实时功耗的值',
  `capping_target` float(6,2) NOT NULL COMMENT 'cpu的capping目标',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间，记录capping动作的时间',
  PRIMARY KEY (`cpu_capping_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cpu
-- ----------------------------
DROP TABLE IF EXISTS `cpu`;
CREATE TABLE `cpu`  (
  `cpu_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'cpu主键id',
  `cpu_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '服务器名称，信息描述',
  `cpu_tdp` int(5) NOT NULL COMMENT 'cpu的tdp的值',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`cpu_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for cpu_power
-- ----------------------------
DROP TABLE IF EXISTS `cpu_power`;
CREATE TABLE `cpu_power`  (
  `cpu_power_id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'cpu实时功耗id',
  `cpu_power_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT 'cpu实时功耗名称，信息描述',
  `cpu_id` int(10) NOT NULL COMMENT 'cpu id（外键）',
  `cpu_power` float(6,2) NOT NULL COMMENT 'cpu的实时功耗的值',
  `cpu_usage` float(6,2) NOT NULL COMMENT 'cpu的利用率',
  `cpu_temperature` float(6,2) NOT NULL COMMENT 'cpu的温度',
  `is_del` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '是否删除(0:未删除；1:已删除)',
  `create_date` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`cpu_power_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

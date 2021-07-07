-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ip_order_db
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int DEFAULT NULL,
  `id_client` int DEFAULT NULL,
  `str_adr` varchar(256) DEFAULT NULL,
  `comment` varchar(256) DEFAULT NULL,
  `full_name` varchar(256) DEFAULT NULL,
  `geo_code_1` double DEFAULT NULL,
  `geo_code_2` double DEFAULT NULL,
  `phone` varchar(24) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (2,1,'Тверь, Спартака, 22','Основной','Петров Петр',56.850535,35.881668,'+79876543210'),(3,1,'Тверь, Макарова, 15','Дополнительный','Иванов Иван',56.847799,35.887902,'+71234567890'),(4,1,'Москва','Комментарий','Аня Мирченко',55.6831438540624,37.6825763299159,'+79693439977'),(5,1,'Ступино','11111111111','Денис Смиянов',54.873927871614,38.1574105734659,'+74564534455'),(56,4,'Москва, Судостроительная, 24','','Александр Петров',55.6831438540624,37.6825763299159,'+74567890000'),(57,4,'Ступино, Вертолётная, 40','','Алексей Смирнов',54.873927871614,38.1574105734659,'+79008007060'),(58,4,'Тверь, Макарова, 15','','Михаил Михайлов',56.847799,35.887902,'+76007009080'),(59,4,'Тверь, Спартака, 22','','Алексей Алексеев',56.850535,35.881668,'+79001002030'),(60,1,'Москва, Большая Семёновская, 38','','Денис Петров',55.78133292112731,37.70992589951107,'+76786785645'),(61,1,'Ступино','','Михаил Петров',55.78274625281619,37.719598710447734,'+78008008080'),(64,1,'Москва','комментарий','Анна Мирченко',55.800217744487156,37.79335992749116,'889798789879'),(65,1,'Ступино','комментарий 2','Денис Смиянов',55.76811251346744,37.59692736926361,'6648686868'),(66,1,'Москва','','Иванов Иван',55.7675802585307,37.59783932032865,'454564'),(67,1,'Ступино','','Петр Сидоров',55.70830378095172,37.68073656120028,'44546545'),(68,1,'Ступино, Горького, 26','','Иван Петров',54.8911424994513,38.06259898968368,'+79008007060'),(69,1,'Ступино, Калинина, 34 ','','Петр Иванов',54.89186622472681,38.06910070980772,'+78009001020'),(70,5,'Москва','укцук','Анна',55.736016931931935,37.61313130134487,'89798797'),(71,5,'Ступино','','Ольга',55.73422511091178,37.663835780562366,'9878798789'),(72,1,'Ступино, Победы 26/52',NULL,'Денис Смиянов',54.892096,38.079681,'+79007006050'),(73,1,'Ступино, Победы, 34',NULL,'Иван Иванов',54.895354,38.08034,'+79008006050'),(74,6,'Москва','','',0,0,''),(75,6,'Ступино','','',0,0,'');
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!50001 DROP VIEW IF EXISTS `order_details`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `order_details` AS SELECT 
 1 AS `courier_id`,
 1 AS `order_num_from`,
 1 AS `order_date`,
 1 AS `client_id`,
 1 AS `cost`,
 1 AS `adr_from`,
 1 AS `geo_code_1_from`,
 1 AS `geo_code_2_from`,
 1 AS `full_name_from`,
 1 AS `phone_from`,
 1 AS `order_num_to`,
 1 AS `adr_to`,
 1 AS `geo_code_1_to`,
 1 AS `geo_code_2_to`,
 1 AS `full_name_to`,
 1 AS `phone_to`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `order_statuses`
--

DROP TABLE IF EXISTS `order_statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_statuses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_status` varchar(64) NOT NULL,
  `status_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status_reason` varchar(256) DEFAULT NULL,
  `order_num` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_statuses_orders_order_num_fk` (`order_num`),
  KEY `order_statuses_typical_order_statuses_status_name_fk` (`order_status`),
  CONSTRAINT `order_statuses_orders_order_num_fk` FOREIGN KEY (`order_num`) REFERENCES `orders` (`order_num`),
  CONSTRAINT `order_statuses_typical_order_statuses_status_name_fk` FOREIGN KEY (`order_status`) REFERENCES `typical_order_statuses` (`status_name`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_statuses`
--

LOCK TABLES `order_statuses` WRITE;
/*!40000 ALTER TABLE `order_statuses` DISABLE KEYS */;
INSERT INTO `order_statuses` VALUES (1,'Курьер найден','2021-06-08 13:32:42',NULL,1),(49,'Заказ создан','2021-06-15 23:41:52',NULL,2),(70,'Заказ создан','2021-06-16 15:54:35',NULL,23),(71,'Курьер найден','2021-06-16 16:32:33',NULL,2),(72,'Посылка принята курьером','2021-06-16 16:32:44',NULL,2),(73,'Заказ выполнен','2021-06-16 16:33:11',NULL,2),(74,'Заказ создан','2021-06-17 01:22:10',NULL,24),(75,'Заказ создан','2021-06-17 08:15:49',NULL,25),(77,'Посылка принята курьером','2021-06-17 08:47:32',NULL,1),(78,'Заказ создан','2021-06-17 08:48:22',NULL,27),(79,'Курьер найден','2021-06-17 08:49:38',NULL,27),(80,'Посылка принята курьером','2021-06-17 08:50:11',NULL,27),(81,'Заказ выполнен','2021-06-17 08:50:29',NULL,27),(82,'Заказ создан','2021-06-17 09:50:21',NULL,28),(83,'Курьер найден','2021-06-17 20:34:54',NULL,28),(84,'Посылка принята курьером','2021-06-17 20:35:15',NULL,28),(85,'Заказ выполнен','2021-06-17 20:35:37',NULL,28),(86,'Заказ создан','2021-06-17 20:43:11',NULL,29),(87,'Курьер найден','2021-06-18 09:07:29',NULL,23),(88,'Заказ создан','2021-06-18 11:06:02',NULL,30),(89,'Курьер найден','2021-06-18 11:40:03',NULL,30),(90,'Курьер найден','2021-06-18 12:01:53',NULL,25),(91,'Посылка принята курьером','2021-06-18 12:02:09',NULL,25),(92,'Заказ выполнен','2021-06-18 12:02:12',NULL,25),(93,'Курьер найден','2021-06-18 12:41:34',NULL,29),(94,'Курьер найден','2021-06-18 12:42:12',NULL,31),(96,'Заказ выполнен','2021-06-18 12:43:19',NULL,31),(97,'Курьер найден','2021-06-19 20:40:23',NULL,24),(98,'Посылка принята курьером','2021-06-19 20:40:43',NULL,24),(99,'Заказ выполнен','2021-06-19 20:40:58',NULL,24),(100,'Заказ создан','2021-06-22 13:03:18',NULL,32),(101,'Курьер найден','2021-07-02 13:45:13',NULL,31),(102,'Посылка принята курьером','2021-07-02 13:45:43',NULL,31),(103,'Заказ выполнен','2021-07-02 13:46:49',NULL,31),(104,'Курьер найден','2021-07-02 13:47:13',NULL,31),(105,'Посылка принята курьером','2021-07-02 13:48:15',NULL,31),(106,'Заказ выполнен','2021-07-02 13:51:48',NULL,31),(107,'Курьер найден','2021-07-02 13:52:05',NULL,31),(108,'Посылка принята курьером','2021-07-02 13:52:28',NULL,31),(109,'Заказ выполнен','2021-07-02 13:53:38',NULL,31),(110,'Курьер найден','2021-07-02 13:53:58',NULL,31),(111,'Посылка принята курьером','2021-07-02 13:54:15',NULL,31),(112,'Заказ выполнен','2021-07-02 13:55:39',NULL,31),(113,'Курьер найден','2021-07-02 13:55:56',NULL,31),(114,'Посылка принята курьером','2021-07-02 13:56:14',NULL,31),(115,'Заказ выполнен','2021-07-02 14:18:56',NULL,31);
/*!40000 ALTER TABLE `order_statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_num` int NOT NULL AUTO_INCREMENT,
  `client_id` int NOT NULL,
  `courier_id` int DEFAULT NULL,
  `sent_from_id` int NOT NULL,
  `sent_to_id` int NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cost` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_num`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,1,2,3,'2021-06-08 10:25:36',200.00),(2,1,1,4,5,'2021-06-15 20:41:49',500.00),(23,4,2,56,57,'2021-06-16 12:54:35',0.00),(24,4,1,58,59,'2021-06-16 22:22:10',0.00),(25,1,1,60,61,'2021-06-17 05:15:49',62.00),(27,1,1,64,65,'2021-06-17 05:48:22',1279.00),(28,1,1,66,67,'2021-06-17 06:50:21',839.00),(29,1,1,68,69,'2021-06-17 17:43:11',42.00),(30,5,2,70,71,'2021-06-18 08:06:02',318.00),(31,1,1,72,73,'2021-06-18 09:37:13',100.00),(32,6,NULL,74,75,'2021-06-22 10:03:18',0.00);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typical_order_statuses`
--

DROP TABLE IF EXISTS `typical_order_statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typical_order_statuses` (
  `status_name` varchar(64) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`status_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typical_order_statuses`
--

LOCK TABLES `typical_order_statuses` WRITE;
/*!40000 ALTER TABLE `typical_order_statuses` DISABLE KEYS */;
INSERT INTO `typical_order_statuses` VALUES ('Заказ выполнен',NULL),('Заказ создан',''),('Курьер найден',NULL),('Посылка принята курьером','');
/*!40000 ALTER TABLE `typical_order_statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `order_details`
--

/*!50001 DROP VIEW IF EXISTS `order_details`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `order_details` AS select `sent_from`.`courier_id` AS `courier_id`,`sent_from`.`order_num_from` AS `order_num_from`,`sent_from`.`order_date` AS `order_date`,`sent_from`.`client_id` AS `client_id`,`sent_from`.`cost` AS `cost`,`sent_from`.`adr_from` AS `adr_from`,`sent_from`.`geo_code_1_from` AS `geo_code_1_from`,`sent_from`.`geo_code_2_from` AS `geo_code_2_from`,`sent_from`.`full_name_from` AS `full_name_from`,`sent_from`.`phone_from` AS `phone_from`,`sent_to`.`order_num_to` AS `order_num_to`,`sent_to`.`adr_to` AS `adr_to`,`sent_to`.`geo_code_1_to` AS `geo_code_1_to`,`sent_to`.`geo_code_2_to` AS `geo_code_2_to`,`sent_to`.`full_name_to` AS `full_name_to`,`sent_to`.`phone_to` AS `phone_to` from ((select `orders`.`courier_id` AS `courier_id`,`orders`.`order_num` AS `order_num_from`,`orders`.`order_date` AS `order_date`,`orders`.`client_id` AS `client_id`,`orders`.`cost` AS `cost`,`addresses`.`str_adr` AS `adr_from`,`addresses`.`geo_code_1` AS `geo_code_1_from`,`addresses`.`geo_code_2` AS `geo_code_2_from`,`addresses`.`full_name` AS `full_name_from`,`addresses`.`phone` AS `phone_from` from (`orders` join `addresses`) where (`orders`.`sent_from_id` = `addresses`.`id`)) `sent_from` join (select `orders`.`order_num` AS `order_num_to`,`addresses`.`str_adr` AS `adr_to`,`addresses`.`geo_code_1` AS `geo_code_1_to`,`addresses`.`geo_code_2` AS `geo_code_2_to`,`addresses`.`full_name` AS `full_name_to`,`addresses`.`phone` AS `phone_to` from (`orders` join `addresses`) where (`orders`.`sent_to_id` = `addresses`.`id`)) `sent_to` on((`sent_from`.`order_num_from` = `sent_to`.`order_num_to`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-06 13:17:36

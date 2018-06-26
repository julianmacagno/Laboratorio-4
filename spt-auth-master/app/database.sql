-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: julian
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit_events`
--

DROP TABLE IF EXISTS `audit_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `event_id` varchar(50) NOT NULL,
  `event_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_events`
--

LOCK TABLES `audit_events` WRITE;
/*!40000 ALTER TABLE `audit_events` DISABLE KEYS */;
INSERT INTO `audit_events` VALUES (1,'julianmacagno','Successful Login','2018-06-25 22:14:38'),(2,'julianmacagno','Successful Login','2018-06-25 22:17:24'),(3,'julianmacagno','Successful Login','2018-06-25 22:21:01'),(4,'julianmacagno','Successful Login','2018-06-25 22:22:11'),(5,'julianmacagno','Successful Login','2018-06-25 22:23:25'),(6,'julianmacagno','Successful Login','2018-06-25 22:24:30'),(7,'julianmacagno','Successful Login','2018-06-25 22:26:00'),(8,'julianmacagno','Successful Login','2018-06-25 22:26:41'),(9,'julianmacagno','Successful Login','2018-06-25 22:27:31'),(10,'julianmacagno','Successful Login','2018-06-25 22:28:25'),(11,'julianmacagno','Successful Login','2018-06-25 22:29:43'),(12,'julianmacagno','Successful Login','2018-06-25 22:30:41'),(13,'julianmacagno','Successful Login','2018-06-25 22:33:05'),(14,'julianmacagno','Successful Login','2018-06-25 22:55:54'),(15,'julianmacagno','Successful Login','2018-06-26 17:35:11'),(16,'julianmacagno','Successful Login','2018-06-26 17:46:42'),(17,'julianmacagno','Successful Login','2018-06-26 17:57:10'),(18,'julianmacagno','Successful Login','2018-06-26 18:12:23'),(19,'julianmacagno','Successful Login','2018-06-26 18:24:39'),(20,'admin','Successful Registration','2018-06-26 18:39:25'),(21,'bruno','Successful Registration','2018-06-26 18:41:47'),(22,'bruno','Successful Registration','2018-06-26 18:45:05'),(23,'julianmacagno','Successful Login','2018-06-26 18:51:26'),(24,'julianmacagno','Successful Login','2018-06-26 18:54:22'),(25,'admin','Successful Login','2018-06-26 19:00:28'),(26,'admin','Successful Logout','2018-06-26 19:02:20'),(27,'julianmacagno','Successful Login','2018-06-26 19:02:24'),(28,'julianmacagno','Successful Login','2018-06-26 19:07:22'),(29,'julianmacagno','Successful Logout','2018-06-26 19:08:29'),(30,'julianmacagno','Successful Logout','2018-06-26 19:11:09'),(31,'julianmacagno','Successful Login','2018-06-26 19:11:14'),(32,'julianmacagno','Successful Logout','2018-06-26 19:11:25'),(33,'bruno','Successful Login','2018-06-26 19:11:34'),(34,'bruno','Successful Logout','2018-06-26 19:11:43');
/*!40000 ALTER TABLE `audit_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credentials`
--

DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credentials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `admin` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES (1,'julianmacagno','rivadavia850','N'),(2,'julian','rivadavia850','N'),(4,'lucas','rivadavia850','N'),(5,'emanuel','rivadavia850','N'),(8,'diego','rivadavia850','N'),(11,'gaston','rivadavia850','N'),(12,'javier','rivadavia850','N'),(13,'enzo','rivadavia850','N'),(14,'admin','rivadavia850','S'),(16,'bruno','rivadavia850','N');
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-26 19:14:50

-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: showerthoughts
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `current`
--

DROP TABLE IF EXISTS `current`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current` (
  `id` char(6) COLLATE utf8mb4_bin NOT NULL,
  `score` int(11) DEFAULT NULL,
  `title` varchar(512) COLLATE utf8mb4_bin DEFAULT NULL,
  `date_added` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current`
--

LOCK TABLES `current` WRITE;
/*!40000 ALTER TABLE `current` DISABLE KEYS */;
/*!40000 ALTER TABLE `current` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorited_tweets`
--

DROP TABLE IF EXISTS `favorited_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorited_tweets` (
  `status` bigint(20) NOT NULL,
  `date_added` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorited_tweets`
--

LOCK TABLES `favorited_tweets` WRITE;
/*!40000 ALTER TABLE `favorited_tweets` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorited_tweets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `following`
--

DROP TABLE IF EXISTS `following`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `following` (
  `id` bigint(20) NOT NULL,
  `date_added` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `following`
--

LOCK TABLES `following` WRITE;
/*!40000 ALTER TABLE `following` DISABLE KEYS */;
/*!40000 ALTER TABLE `following` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `my_followers`
--

DROP TABLE IF EXISTS `my_followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `my_followers` (
  `id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `my_followers`
--

LOCK TABLES `my_followers` WRITE;
/*!40000 ALTER TABLE `my_followers` DISABLE KEYS */;
INSERT INTO `my_followers` VALUES (940187414097776640);
/*!40000 ALTER TABLE `my_followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `my_followers_cursor`
--

DROP TABLE IF EXISTS `my_followers_cursor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `my_followers_cursor` (
  `who` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL,
  `next_cursor` bigint(20) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `my_followers_cursor`
--

LOCK TABLES `my_followers_cursor` WRITE;
/*!40000 ALTER TABLE `my_followers_cursor` DISABLE KEYS */;
INSERT INTO `my_followers_cursor` VALUES ('wetphone',0);
/*!40000 ALTER TABLE `my_followers_cursor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `names`
--

DROP TABLE IF EXISTS `names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `names` (
  `id` char(6) COLLATE utf8mb4_bin NOT NULL,
  `date_added` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `names`
--

LOCK TABLES `names` WRITE;
/*!40000 ALTER TABLE `names` DISABLE KEYS */;
/*!40000 ALTER TABLE `names` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-11 17:27:57

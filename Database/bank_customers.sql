-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: bank
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `accNo` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `accType` varchar(1) NOT NULL,
  `birthDate` date NOT NULL,
  `age` varchar(3) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `country` varchar(60) NOT NULL,
  `nationalID` varchar(14) NOT NULL,
  `pin` varchar(4) NOT NULL,
  `balance` float NOT NULL,
  `creation_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`accNo`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Ahmed Amr AbdEl-Rafaa Rizk','S','2000-12-15','20','01119597740','M','Egypt','30012151601673','1478',6001000,'2021-08-15 00:00:00'),(3,'Abd-Ullah Asharaf Mohammed','C','2000-02-18','20','01068044372','M','Egypt','30002180102296','8489',10000,'2021-08-15 00:00:00'),(4,'AbdEl-Rahman Sayed','S','2001-06-27','20','01066772962','M','Egypt','30106250105073','2224',150000,'2021-12-21 23:16:20'),(5,'AbdEl-Zaher Walid AbdEl-Zaher ','C','2001-03-02','20','01553708896','M','Egypt','30103022100295','8896',7560,'2021-12-20 00:13:31'),(6,'Abd-Ullah Fahmy Mohamed ','C','2000-11-20','20','01029700390','M','Egypt','30011208800252','9914',98600,'2021-08-15 00:00:00'),(7,'AbdEl-Rhman Mohamed Abdelrhman Ahmed','S','2001-01-15','20','01063749458','M','Egypt','30101150103733','7154',554100,'2021-08-15 00:00:00'),(8,'Malik AbdEl-Zaher Walid','S','2003-02-01','20','01110492115','M','Egypt','30103022122295','1254',900,'2021-08-15 00:00:00'),(9,'AbdEl-Khalek Mahmoud Mohamed','S','2001-05-17','20','01156129973','M','Egypt','30105171402256','5555',980640,'2021-12-25 19:35:44'),(34,'Osama El-Said','S','2001-06-15','20','01119591403','M','Egypt','30012151601616','5555',98700,'2021-12-26 00:36:45');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-29  2:50:58

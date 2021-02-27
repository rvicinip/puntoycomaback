-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: bpmdb
-- ------------------------------------------------------
-- Server version	5.7.12-log

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
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresa` (
  `nit` varchar(20) NOT NULL COMMENT 'Número de identificación de la emoresa',
  `nombre` varchar(200) NOT NULL COMMENT 'Nombre de la empresa',
  `niveles` int(11) NOT NULL COMMENT 'Cantidad de niveles que manejará la empresa',
  `estado` varchar(3) DEFAULT NULL COMMENT 'Estado en que se encuentra la empresa A(activo) D(inactiva)',
  `tipo` varchar(10) DEFAULT NULL COMMENT 'Rol de la empresa en la aplicación',
  PRIMARY KEY (`nit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `id_usuario` varchar(20) NOT NULL COMMENT 'Numero de documento de identidad del usuario y login del mismo',
  `nombre` varchar(200) NOT NULL COMMENT 'Nombre completo del usuario',
  `empresa` varchar(20) NOT NULL COMMENT 'Identificador de la empresa a la que pertenece el usuario',
  `clave` varchar(300) NOT NULL COMMENT 'Contraseña de ingreso del usuario',
  `email` varchar(100) DEFAULT NULL COMMENT 'Correo electrónico del usuario',
  `cargo` varchar(50) DEFAULT NULL COMMENT 'Cargo que desempeña en la empresa',
  `salario` int(11) DEFAULT NULL COMMENT 'Remuneración económica que recibe el empleado',
  `jornada` varchar(10) DEFAULT NULL COMMENT 'Tipo de jornada que realiza el empleado',
  `perfil` varchar(10) DEFAULT NULL COMMENT 'Nombre de los privilegios que tiene el usuario dentro de la aplicación',
  `ccostos` varchar(50) DEFAULT NULL COMMENT 'Centro de constos al que está afiliado el trabajador',
  `termino` varchar(10) DEFAULT NULL COMMENT 'Tipo de contrato de trabajo',
  `estado` varchar(3) DEFAULT NULL COMMENT 'Estatus dentro de la aplicación del usuario A(activo) D(inactivo)',
  `codigo` int(11) DEFAULT NULL COMMENT 'Campo para validar la recuperación de contraseña',
  `estadoEncuesta` varchar(3) DEFAULT 'P' COMMENT 'Estado del desarrollo de la encuesta del usuario, "P"(Pendiente), "D"(Desarrollo), "T"(Terminado)',
  PRIMARY KEY (`id_usuario`),
  KEY `FK_Empresa_Usuario_idx` (`empresa`),
  CONSTRAINT `FK_Empresa_Usuario` FOREIGN KEY (`empresa`) REFERENCES `empresa` (`nit`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tabla de los usuarios del sistema de bpmdb';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

--
-- Table structure for table `consultor`
--

DROP TABLE IF EXISTS `consultor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consultor` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Código principal de identificación',
  `empresa` varchar(20) NOT NULL COMMENT 'Relaciona la empresa asociada',
  `consultor` varchar(20) NOT NULL COMMENT 'Relaciona el consultor asociado',
  `estado` varchar(3) DEFAULT NULL COMMENT 'Define el estado de la relación A(activo) D(inactivo)',
  PRIMARY KEY (`id`),
  KEY `FK_Empresa_Consultor_idx` (`empresa`),
  KEY `FK_Usuario_Consultor_idx` (`consultor`),
  CONSTRAINT `FK_Empresa_Consultor` FOREIGN KEY (`empresa`) REFERENCES `empresa` (`nit`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_Usuario_Consultor` FOREIGN KEY (`consultor`) REFERENCES `usuario` (`id_usuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diccionario`
--

DROP TABLE IF EXISTS `diccionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diccionario` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Id de la actividad del diccionario',
  `id_actividad` varchar(15) NOT NULL COMMENT 'Id de reconocimiento de la actividad en la empresa',
  `nombre` varchar(200) NOT NULL COMMENT 'Nombre de la actividad',
  `empresa` varchar(20) NOT NULL COMMENT 'Relaciona la empresa a la que eprtenece la actividad',
  `nivel` int(11) NOT NULL COMMENT 'Indicador del nivel al que pertenece la actividad',
  `padre` int(11) DEFAULT NULL COMMENT 'Relaciona el id del padre al que pertenece la actividad',
  `descripcion` varchar(300) DEFAULT NULL COMMENT 'Contiene la descripción de la actividad',
  `mas` varchar(20) DEFAULT NULL COMMENT 'Manual, Automática, Semiautomática',
  `ceno` varchar(20) DEFAULT NULL COMMENT 'Crítica, Escencial, No Escencial, Opcional',
  `tipo` varchar(20) DEFAULT NULL COMMENT 'Clasificación de la actividad dentro de la empresa',
  `cadena_de_valor` varchar(20) DEFAULT NULL COMMENT 'Donde aporta valor a la empresa la actividad',
  PRIMARY KEY (`id`),
  KEY `FK_Empresa_Diccionario_idx` (`empresa`),
  KEY `FK_Padre_Diccionario_idx` (`padre`),
  CONSTRAINT `FK_Empresa_Diccionario` FOREIGN KEY (`empresa`) REFERENCES `empresa` (`nit`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_Padre_Diccionario` FOREIGN KEY (`padre`) REFERENCES `diccionario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Contiene el diccionario de actividades de la empresa';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `frecuencia`
--

DROP TABLE IF EXISTS `frecuencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `frecuencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador del registro',
  `nombre` varchar(200) NOT NULL COMMENT 'Nombre de la frecuencia',
  `tipo` int(11) NOT NULL COMMENT 'Clasificación de la frecuencia',
  `valor` float NOT NULL COMMENT 'Valor correspondiente a la frecuencia',
  `empresa` varchar(20) NOT NULL COMMENT 'Empresa a la que pertenece la frecuencia',
  `unidad` varchar(15) DEFAULT NULL COMMENT 'Unidad de medida de la frecuencia',
  PRIMARY KEY (`id`),
  KEY `FK_Empresa_Frecuencia_idx` (`empresa`),
  CONSTRAINT `FK_Empresa_Frecuencia` FOREIGN KEY (`empresa`) REFERENCES `empresa` (`nit`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Unidades de medida y periodos de frecuencia de las tareas';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `encuesta`
--

DROP TABLE IF EXISTS `encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encuesta` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Identificador de la respuesta',
  `actividad` int(11) NOT NULL COMMENT 'Relaciona la actividad del diccionario a la que se le está definiento el tiempo',
  `usuario` varchar(20) NOT NULL COMMENT 'Relaciona el empleado que responde la encuesta',
  `cantidad` int(11) NOT NULL COMMENT 'Contiene la respuesta de la encuesta sobre la actividad',
  `tiempo` float NOT NULL COMMENT 'Cálculo de multiplicar la cantidad por el valor del tiempo (umedida) asociado en su correspondiente valor',
  `umedida` int(11) NOT NULL COMMENT 'Relaciona la unidad de tiempo con la tabla de frecuencias',
  `frecuencia` int(11) NOT NULL COMMENT 'Relaciona la frecuencia con la tabla de frecuencias para el rango de realización de la actividad',
  `Jornada` float DEFAULT NULL COMMENT 'Calculo de la jornada del empleado, se obtiene de la suma de todos los tiempos de las actividades',
  `fteAct` float DEFAULT NULL COMMENT 'Cálculo del FTE de la actividad',
  `fteUser` float DEFAULT NULL COMMENT 'Cálculo del FTE del empleado',
  `valorAct` float DEFAULT NULL COMMENT 'Cálculo del valor de la actividad realizada',
  `estado` varchar(3) DEFAULT NULL COMMENT 'Estado en que se encuentra el registro A(activo) D(Eliminado)',
  PRIMARY KEY (`id`),
  KEY `FK_Usuario_Encuesta_idx` (`usuario`),
  KEY `FK_Frecuencia_Encuesta_idx` (`frecuencia`),
  KEY `FK_Tiempo_Encuesta_idx` (`umedida`),
  CONSTRAINT `FK_Frecuencia_Encuesta` FOREIGN KEY (`frecuencia`) REFERENCES `frecuencia` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_Tiempo_Encuesta` FOREIGN KEY (`umedida`) REFERENCES `frecuencia` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_Usuario_Encuesta` FOREIGN KEY (`usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Contiene las respuesta de los empleados al reporte de tiempos';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-27  8:21:21

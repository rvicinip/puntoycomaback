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
-- Dumping data for table `empresa`
--

LOCK TABLES `empresa` WRITE;
/*!40000 ALTER TABLE `empresa` DISABLE KEYS */;
INSERT INTO `empresa` VALUES ('900222444','Fabrica de innovación SAS',3,'A','client'),('910210059','Inversiones Velasquez Naranjo y Cia',3,'A','admon');
/*!40000 ALTER TABLE `empresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES ('1017136558','Manuela Rodriguez','900222444','$2b$12$7j5KzR1JLm33YjCsiT44bOs/Z1wP1zmeRQxqDKZsrBL2BGJUmS/pa','mrodriguez@venaycia.com','Consultora Junior',1800000,'Diurna','client','2','Indefinido','A',0,'Pendiente'),('1017175942','Luisa Hoyos','900222444','$2b$12$Hl3oZNXsm/5CK2xmJ/GznedsjQmZaWILLpSzOcvhKlxER/WErRT2C','lhoyos@venaycia.com','Consultora Junior',1500000,'Diurna','client','2','Indefinido','A',0,'Pendiente'),('1022333444','Paula Pelaez','910210059','$2b$12$Q6RidR0eelibD5w0TB0sSOPsGWg/TRFohJj3jBMpByt1YNpcMliLy','','Consultora',0,'diurna','consult','','','A',0,NULL),('1033444555','Alvaro Pelaez','910210059','$2b$12$olYc9HMEen9T.9vpOLPeD.1lcq/8yP5a37F5g5OF0kpxF3LyTO5IC','wacor@vitt.co','Consultor',0,'diurna','consult','','','A',0,NULL),('1044555666','Juliana Gomez','910210059','$2b$12$SVyT/HujK/NM5daQ5W1/6.dlMXnlsw3.Joy0EDpPlMaXzDKIbE6ry','','Consultora',0,'diurna','consult','','','A',0,NULL),('32256494','Isabel Narajo','900222444','$2b$12$hrR/AqlxPh/GNjgPASd8tebBLqLN7SAs8mfT7xGpjhlaUnhLokAha','inaranjo@venaycia.com','Administrativa',1500000,'Diurna','client','1','Indefinido','A',0,'Pendiente'),('43221806','Natalia Ramirez','900222444','$2b$12$3Hc3B5sazGeDt.FEmjOnneD1JupSdt9A46RO2z7/pMqlGO9xx8xEe','nramirez@venaycia.com','Consultora Senior',2000000,'Diurna','client','2','Indefinido','A',0,'Pendiente'),('43874999','Catalina Rave','900222444','$2b$12$9yuQYhZeSakIUNrpCnB0duxa2Xl2KbNmEE1h0RtvLHpEURJkVTNo6','crave@venaycia.com','Consultora Senior',2000000,'Diurna','client','2','Indefinido','A',0,'Pendiente'),('71788316','Alvaro Fernando Velasquez','910210059','$2b$12$wi/lw0A1aTcedTqdPoSLA.G383AyaZOfoDGU5/WbKK7HwpXteaLsu','','Gerente',0,'','director','','','A',0,NULL),('8358473','Juan Chavarriaga','900222444','$2b$12$OPxycyDf8BvTiRbqm/w45O4SJxwey/xEIDMV6Fd0XRw86qy2Vze3q','jchavarriaga@venaycia.com','Consultora Junior',1500000,'Diurna','client','2','Indefinido','A',0,'Pendiente');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

--
-- Dumping data for table `consultor`
--

LOCK TABLES `consultor` WRITE;
/*!40000 ALTER TABLE `consultor` DISABLE KEYS */;
/*!40000 ALTER TABLE `consultor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `diccionario`
--

LOCK TABLES `diccionario` WRITE;
/*!40000 ALTER TABLE `diccionario` DISABLE KEYS */;
INSERT INTO `diccionario` VALUES (277,'001','PLANEACIÓN ','900222444',1,'',NULL,NULL,NULL,NULL,NULL,NULL),(278,'001001','Planeación estratégica','900222444',2,'001',277,NULL,NULL,NULL,NULL,NULL),(279,'001001001','Planeación estratégica','900222444',3,'001001',278,NULL,NULL,NULL,NULL,NULL),(280,'001001002','Planeación anual operativa','900222444',3,'001001',278,'Elaborar los planes anuales que contengan la descripción de las actividades a realizar por cada una de las áreas',NULL,NULL,NULL,NULL),(281,'001001003','Gerencia de proyectos','900222444',3,'001001',278,'Establecer la asignación del recursos (Humanos, técnicos y económicos) para el desarrollo de los planes e identificar otras necesidades.',NULL,NULL,NULL,NULL),(282,'001001001001','Definición o revisión de misión','900222444',4,'001001001',279,'En las reapreciaciones anuales realizadas por el comité de Planeación se revisa la Misión de acuerdo al entorno actual y a las condiciones de la Cooperativa en el momento de la revisión','Manual','Critica','Admin','Estrategia'),(283,'001001001010','Socialización del plan estratégico o sus actualizaciones','900222444',4,'001001001',279,'Una vez culminada el plan estratégico o sus ajustes este debe darse a conocer a la organización mediante los mecanismos que se determinen, bien sea electrónico o escrito.','Manual','Critica','Admin','Estrategia'),(284,'001001001011','Seguimiento y control plan estrategico ','900222444',4,'001001001',279,'Los miembros de comité de planeación a través de la herramienta de planeación sp deberán realizar el seguimiento a la planeación verificando el cumplimiento de los objetivos a través de los monitoreos de los indicadores y de los planes que fueron definidos para materializar las estrategias.','Manual','Critica','Admin','Estrategia'),(285,'001001001012','Control y seguimiento proyectos','900222444',4,'001001001',279,'Controlar la ejecución de los proyectos estratégicos','Manual','Critica','Admin','Estrategia'),(286,'001001001002','Definición o revisión de visión','900222444',4,'001001001',279,'En las reapreciaciones anuales realizadas por el comité de Planeación se revisa la Misión de acuerdo al entorno actual y a las condiciones de la Cooperativa en el momento de la revisión','Manual','Critica','Admin','Estrategia'),(287,'001001001003','Identificación escenarios','900222444',4,'001001001',279,'Se reúne el comité de planeación estratégica  y evalúa los valores actuales de la Cooperativa y teniendo encuesta los cambio que se han dado y para dar respuesta a la misión y visión propuesta se revisan y se proponen nuevos o se reafirman los existentes si aun aplican (se realiza en la revisión trianual)','Manual','Critica','Admin','Estrategia'),(288,'001001001004','Definición de matriz floa','900222444',4,'001001001',279,'El comité de planeación estratégica identifica las variables  macroeconómicas que puedan impactar a CFA y  los escenarios que puedan responder al planteamiento de misión y visión.A través de los escenarios se trata de visualizar el futuro de la Cooperativa tomando como referencia las variables económicas, políticas, sociales y tecnológicas que previamente son discutidas a  través de talleres.Los escenarios se  plantean desde  la perspectiva  de alta incidencia y ocurrencia y lo positivo o negativo, la interrelación de las variables que fueron objeto de análisis. Los escenarios se dejan descritos en el documento de plan estratégico','Manual','Critica','Admin','Estrategia'),(289,'001001001005','Definición objetivos','900222444',4,'001001001',279,'Teniendo en cuenta la descripción de los escenarios y las variables con las cuales fueron construidos, así como aspectos internos de la organización se elabora la matriz FLOA (DOFA)  cual debe contener como máximo diez aspectos por cuadrante, el trabajo definitivo se lleva a la herramienta de planeación SP','Manual','Critica','Admin','Estrategia'),(290,'001001001006','Definición indicadores','900222444',4,'001001001',279,'Realizada la actividad anterior, evalúa la matriz y revisan los objetivos estratégicos, tácticos y operativos contenidos en el plan y determinan cuales deberían ser ingresados o modificados  de acuerdo a situación planteada (deben permitir corregir las discontinuidades de la gestión y generar valor para la organización, así como que estén en cumplimiento con la misión y la visión. Los objetivos se seleccionan de acuerdo con las perspectivas del Balanced score card sumando la perspectiva social.','Manual','Critica','Admin','Estrategia'),(291,'001001001007','Definición de estrategias','900222444',4,'001001001',279,' Dada la matriz FLOA y los objetivos realiza cruces para determinar estrategias que es la forma a través de la cual se cumplirán los objetivos de la CooperativaLas estrategias están dadas en los siguientes tipos. Ofensivas (FO) Defensivas (FA) Supervivencia (LA) Reorientación (LO). Una vez se hace el cruce y se determinan las estrategias son ingresadas a la herramienta de Planeación SP','Manual','Critica','Admin','Estrategia'),(292,'001001001008','Despliegue de objetivos','900222444',4,'001001001',279,'Considerando los objetivos y las estrategias, a través de la metodología de despliegue de objetivos se trabaja con cada objetivo y se aplica para cada uno lo siguiente: Definición de las Nuevas Propuestas de Valor para el Cliente. Definición del Nuevo Desempeño de los Procesos (Métrica de Valor). Definición de los Aprendizajes y Desarrollos Necesarios. Definición del Desempeño Financiero. Definición y Formulación de los Proyectos / Acciones Inductoras','Manual','Critica','Admin','Estrategia'),(293,'001001001009','Asignación de recursos','900222444',4,'001001001',279,'Establecer la asignación del recursos (Humanos, técnicos y económicos) para el desarrollo de los planes e identificar otras necesidades.','Manual','Critica','Admin','Estrategia'),(294,'001001002001','Elaborar planes Operativos','900222444',4,'001001002',280,'Controlar la ejecución del plan anual operativo','Manual','Critica','Admin','Estrategia'),(295,'001001002002','Seguimiento y control de planes operativos','900222444',4,'001001002',280,'Definir los parámetros para la formulación de nuevos proyectos','Manual','Critica','Admin','Estrategia'),(296,'001001003001','Formulacion de proyectos','900222444',4,'001001003',281,'Definir los parámetros para la formulación de nuevos proyectos','Manual','Critica','Admin','Estrategia'),(297,'001001003002','Asignación de recursos','900222444',4,'001001003',281,'Llevar un control y seguimiento a los diferentes proyectos','Manual','Critica','Admin','Estrategia'),(298,'001001003003','Gestion de proyectos','900222444',4,'001001003',281,'Capacitar a los Directores de Oficina sobre la parte Normativa del proceso de elecciones, esto incluye lo establecido en el Reglamento al Estatuto y el Estatuto.','Manual','Critica','Admin','Estrategia'),(299,'001001003004','Seguimiento de proyectos','900222444',4,'001001003',281,'Coordinar el proceso desde su inicio hasta el final ','Manual','Critica','Admin','Estrategia');
/*!40000 ALTER TABLE `diccionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `encuesta`
--

LOCK TABLES `encuesta` WRITE;
/*!40000 ALTER TABLE `encuesta` DISABLE KEYS */;
/*!40000 ALTER TABLE `encuesta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `frecuencia`
--

LOCK TABLES `frecuencia` WRITE;
/*!40000 ALTER TABLE `frecuencia` DISABLE KEYS */;
INSERT INTO `frecuencia` VALUES (217,'Minuto',1,0.016667,'900222444','hora'),(218,'Hora',1,1,'900222444','hora'),(219,'Dia',1,8,'900222444','hora'),(220,'Semana',1,40,'900222444','hora'),(221,'Quincena',1,80,'900222444','hora'),(222,'Mes',1,160,'900222444','hora'),(223,'Bimestre',1,320,'900222444','hora'),(224,'Trimestre',1,480,'900222444','hora'),(225,'Semestre',1,960,'900222444','hora'),(226,'Año',1,1920,'900222444','hora'),(227,'Dia',2,1,'900222444','día'),(228,'Semana',2,5,'900222444','día'),(229,'Quincena',2,10,'900222444','día'),(230,'Mes',2,20,'900222444','día'),(231,'Bimestre',2,40,'900222444','día'),(232,'Trimestre',2,60,'900222444','día'),(233,'Semestre',2,120,'900222444','día'),(234,'Año',2,240,'900222444','día');
/*!40000 ALTER TABLE `frecuencia` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-28 11:34:42


CREATE TABLE `course` (
  `Id` varchar(10) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `TeacherID` varchar(20) NOT NULL,
  `Credit` int NOT NULL,
  KEY `fk_teach` (`TeacherID`),
  CONSTRAINT `fk_teach` FOREIGN KEY (`TeacherID`) REFERENCES `teacher` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `student` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `teacher` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


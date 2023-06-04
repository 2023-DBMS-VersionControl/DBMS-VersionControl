CREATE TABLE `student` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int(11) NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `teacher` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `course` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
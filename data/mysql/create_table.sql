CREATE TABLE `employees`.`tblemployee` (
  `Employee_ID` INT NOT NULL AUTO_INCREMENT,
  `Employee_Name` VARCHAR(45) NOT NULL,
  `Employee_Department_ID` INT NOT NULL,
  `Employee_Grade_ID` INT NOT NULL DEFAULT A,
  `Employee_Salary` INT NOT NULL,
  PRIMARY KEY (`Employee_ID`),
  INDEX `FK_Department_ID_idx` (`Employee_Department_ID` ASC) VISIBLE,
  CONSTRAINT `FK_Department_ID`
    FOREIGN KEY (`Employee_Department_ID`)
    REFERENCES ` employees`.`department` (`Department_ID`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE);
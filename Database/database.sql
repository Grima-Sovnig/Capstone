/**********************************************************************************************************************
*                                                                                                                     *
*   database.sql                                                                                                      *
*   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
*   The purpose of this file is to implement the SFTPPipeline database schema.                                        *
*                                                                                                                     *
***********************************************************************************************************************/

CREATE DATABASE SFTPPipeline;


USE SFTPPipeline;

---------------------------------------------------------------------------------------------

CREATE TABLE Presets (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL
    -- Connection_String VARCHAR(255) NOT NULL
) ENGINE = InnoDB;



CREATE TABLE Files (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    File_Path VARCHAR(255) NOT NULL,
    Preset_ID INT,
    FOREIGN KEY (Preset_ID) REFERENCES Presets(ID)
) ENGINE = InnoDB;



CREATE TABLE Connections (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Server VARCHAR(100) NOT NULL,
    Username VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Remote_Directory VARCHAR(250) NOT NULL
) ENGINE = InnoDB;



CREATE TABLE Presets_Connections_Relations (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Preset_ID INT,
    Connection_ID INT,
    FOREIGN KEY (Preset_ID) REFERENCES Presets(ID),
    FOREIGN KEY (Connection_ID) REFERENCES Connections(ID)
) ENGINE = InnoDB;



CREATE TABLE Jobs (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL, -- /tn
    Command VARCHAR(255) NOT NULL, -- /tr
    Schedule VARCHAR(15) NOT NULL, -- /sc
    StartTime VARCHAR(20) NOT NULL, -- /st
    StartDate VARCHAR(20), -- /sd
    EndDate VARCHAR(20), -- /ed
    Preset_ID INT NOT NULL,
    -- Foreign Key: Command line argument -> one to many relationship for Presets --
    FOREIGN KEY (Preset_ID) REFERENCES Presets(ID)
) ENGINE = InnoDB;


-------------------------------------------------------------------------


CREATE TABLE Users (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
) ENGINE = InnoDB;



CREATE TABLE Changelogs (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Calendar DATETIME NOT NULL,
    Message VARCHAR(255) NOT NULL,
    Debug VARCHAR(255)
) ENGINE = InnoDB;
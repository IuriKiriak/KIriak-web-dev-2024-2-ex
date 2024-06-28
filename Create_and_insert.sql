DROP DATABASE exam;

CREATE DATABASE exam;

USE exam;


CREATE TABLE Role(
    RoleID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    RoleName VARCHAR(50), 
		RoleDescription VARCHAR(100)
    );
    
    
CREATE TABLE Users(
    UserID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Login VARCHAR(30) NOT NULL,
    PasswordHash VARCHAR(256) NOT NULL,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    FatherName VARCHAR(30) DEFAULT NULL,
    RoleID INT(11) NOT NULL,
		UNIQUE (Login),
    CreateAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
    );
		
    
CREATE TABLE ImageFiles (
		FileID VARCHAR(100) PRIMARY KEY,
    FileName VARCHAR(100) NOT NULL,
    MIMEType VARCHAR(100) NOT NULL,
    MD5Hash VARCHAR(100) NOT NULL,
    UNIQUE (FileName)
);

CREATE TABLE Bots (
    BotID INT AUTO_INCREMENT PRIMARY KEY,
    FileImageID VARCHAR(100),
    NameBot VARCHAR(50) NOT NULL,
    Description TEXT DEFAULT NULL,
    ShortDescription VARCHAR(200) NOT NULL,
    NameForWhat VARCHAR(50) NOT NULL,
    ReleaseDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Developer VARCHAR(50) DEFAULT NULL,
    UserID INT NOT NULL,
    UNIQUE (NameBot),
    FOREIGN KEY (FileImageID) REFERENCES ImageFiles(FileID)
);


CREATE TABLE Type(
    TypeID INT PRIMARY KEY NOT NULL,
    TypeName VARCHAR(50) NOT NULL
    );
				
  
CREATE TABLE BotsType (
    BotID INT,
    TypeID INT,
    PRIMARY KEY (BotID, TypeID),
    FOREIGN KEY (BotID) REFERENCES Bots(BotID) ON DELETE CASCADE,
    FOREIGN KEY (TypeID) REFERENCES Type(TypeID)
		);

CREATE TABLE ReviewStatus (
    StatusID INT AUTO_INCREMENT PRIMARY KEY,
    StatusName VARCHAR(50) NOT NULL
);

  
CREATE TABLE Reviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY, 
    BotID INT NOT NULL,
    UserID INT NOT NULL,
    Rating INT NOT NULL, 
    TextReviews TEXT,
    PublicationDate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    StatusID INT NOT NULL DEFAULT 1, -- 1 = На рассмотрении
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (BotID) REFERENCES Bots(BotID) ON DELETE CASCADE,
    FOREIGN KEY (StatusID) REFERENCES ReviewStatus(StatusID)
);
		

INSERT INTO ReviewStatus (StatusName) VALUES ('На рассмотрении'), ('Одобрена'), ('Отклонена');

-- добавление роли для пользователей 
INSERT INTO Role(RoleID, RoleName) VALUES(1,"Admin");
		
INSERT INTO Role(RoleID, RoleName) VALUES(2, "moderator");

INSERT INTO Role(RoleID, RoleName) VALUES(3, "user");

-- добавление пользователей 

INSERT INTO Users(UserID,
    Login, PasswordHash,
    FirstName, LastName,
		RoleId)
VALUES (1,
    'admin', SHA2('admin', 256),
    'admin', 'admin', 
		1);
		
		
INSERT INTO Users(
		UserID,
    Login, PasswordHash,
    FirstName, LastName,
		RoleId)
VALUES (2,
    'moderator', SHA2('moderator', 256),
    'moderator', 'moderator', 
		2);
		
		
INSERT INTO Users(UserID,
    Login, PasswordHash,
    FirstName, LastName,
		RoleId)
VALUES (3,
    'user1', SHA2('user1', 256),
    'user1', 'user1', 
		3);
		
-- добавление типов для бота

INSERT INTO Type(TypeID, TypeName)
VALUES (1, "game");

INSERT INTO Type(TypeID, TypeName)
VALUES (2, "app");

INSERT INTO Type(TypeID, TypeName)
VALUES (3, "pro");

INSERT INTO Type(TypeID, TypeName)
VALUES (4, "free");


-- добавление 10 ботов (для отображения на двух страницах)

INSERT INTO Bots(NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot12', "Dota 2",'this is first bot', 1);

SET @last_bot_id = LAST_INSERT_ID();

INSERT INTO BotsType(BotID, TypeID)
VALUES (@last_bot_id, 1);
INSERT INTO BotsType(BotID, TypeID)
VALUES (@last_bot_id, 2);


-- INSERT INTO Files(FileID, FilePath, FileImagePath) VALUES (0, "/app/bot1", "/app/bot1/image.png");


INSERT INTO Reviews(BotID, UserID, Rating, TextReviews)
VALUES (@last_bot_id, 1, 5, "хороший бот");


INSERT INTO Reviews(BotID, UserID, Rating, TextReviews)
VALUES (@last_bot_id, 2, 3, "хороший бот");

INSERT INTO Reviews(BotID, UserID, Rating, TextReviews)
VALUES (@last_bot_id, 3, 4, "хороший бот");

INSERT INTO Reviews(BotID, UserID, Rating, TextReviews)
VALUES (@last_bot_id, 2, 5, "хороший бот");

INSERT INTO Reviews(BotID, UserID, Rating, TextReviews)
VALUES (@last_bot_id, 2, 2, "хороший бот");

-- добавление 9 ботов

-- 1

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot13', 'League of Legends', 'this is second bot', 1);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 2

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot14', 'Counter-Strike', 'this is third bot', 2);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 3 

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot15', 'Overwatch', 'this is fourth bot', 2);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 4

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot16', 'Fortnite', 'this is fifth bot', 3);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 5 

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot17', 'Apex Legends', 'this is sixth bot', 3);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 6

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot18', 'Valorant', 'this is seventh bot', 2);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 7

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot19', 'Minecraft', 'this is eighth bot', 1);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 8

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot20', 'Call of Duty', 'this is ninth bot', 2);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);

-- 9

INSERT INTO Bots (NameBot, NameForWhat, ShortDescription, UserID)
VALUES ('bot21', 'Battlefield', 'this is tenth bot', 3);

INSERT INTO BotsType (BotID, TypeID)
VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 4) + 1);



-- DELETE FROM Bots WHERE BotID = 1;

-- DELETE FROM Files WHERE FileID = 1;

/*
SELECT
    Bots.NameBot,
    NameForWhat,
    GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
    Bots.ReleaseDate,
    Bots.ShortDescription,
    AVG(Reviews.Rating) AS AverageRating,
    COUNT(DISTINCT Reviews.ReviewID) AS ReviewCount,
    Files.FileImagePath,
    Files.FilePath
FROM
    Bots
LEFT JOIN Files ON Bots.BotID = Files.FileID
LEFT JOIN Reviews ON Bots.BotID = Reviews.BotID
LEFT JOIN BotsType ON Bots.BotID = BotsType.BotID
LEFT JOIN Type ON BotsType.TypeID = Type.TypeID
GROUP BY
    Bots.BotID
ORDER BY
    Bots.ReleaseDate
DESC;
*/


/*
INSERT INTO ImageFiles (FileName, MIMEType, MD5Hash) 
VALUES ('generated-uuid', 'image/png', 'd41d8cd98f00b204e9800998ecf8427e');

INSERT INTO Bots (FileImage, NameBot, Description, ShortDescription, NameForWhat, Developer, UserID)
VALUES ('generated-uuid', 'MyBot', 'This is a description', 'Short desc', 'Utility', 'DevName', 1);
*/

        INSERT INTO ImageFiles (FileID, FileName, MIMEType, MD5Hash) 
        VALUES ("6e4aebf1-9a64-4fd4-a0df-b3ccc4286f46", "1SfRHi6mSIk.jpg", "image/jpeg", "20996d83cdf6a9d9b1bbabd28f13ea9b");


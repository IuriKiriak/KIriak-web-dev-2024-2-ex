queries = {
    'SELECT_ALL_BOT_INFO_FOR_CARD': """
        SELECT
            Bots.NameBot,
            GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
            Bots.BotID,
            Bots.ReleaseDate,
            ROUND(AVG(CASE WHEN Reviews.StatusID = 2 THEN Reviews.Rating ELSE NULL END), 1) AS AverageRating,
            COUNT(DISTINCT CASE WHEN Reviews.StatusID = 2 THEN Reviews.ReviewID ELSE NULL END) AS ReviewCount,
            ImageFiles.FileID
        FROM
            Bots
        LEFT JOIN Reviews ON Bots.BotID = Reviews.BotID
        LEFT JOIN BotsType ON Bots.BotID = BotsType.BotID
        LEFT JOIN Type ON BotsType.TypeID = Type.TypeID
        LEFT JOIN ImageFiles ON Bots.FileImageID = ImageFiles.FileID
        GROUP BY
            Bots.ReleaseDate,
            Bots.NameBot,
            Bots.BotID,
            ImageFiles.FileID
        ORDER BY
            ReleaseDate DESC
        LIMIT %s OFFSET %s;
    """,

    'SELECT_BOT_INFO_FOR_SHOW':"""
        SELECT 
            Bots.FileImageID,
            Bots.BotID,
            Bots.NameBot,
            Bots.ShortDescription,
            Bots.Description,
            Bots.Developer,
            Bots.ReleaseDate,
            GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
            ROUND(AVG(Reviews.Rating), 1) AS AverageRating,
            COUNT(DISTINCT Reviews.ReviewID) AS ReviewCount
        FROM
            Bots
        LEFT JOIN Reviews ON Bots.BotID = Reviews.BotID
        LEFT JOIN BotsType ON Bots.BotID = BotsType.BotID
        LEFT JOIN Type ON BotsType.TypeID = Type.TypeID
        WHERE
            Bots.BotID = %s
        GROUP BY
            Bots.BotID, Bots.ReleaseDate;
    """,

    "DELETE_BOT_IN_BOTS_TABLE": """
        DELETE FROM ImageFiles
        WHERE FileID = %s;
    """,

    "SELECT_TYPES": """
        SELECT 
            Type.TypeName
        From Type;
    """,

    "INSERT_BOT": """
    INSERT INTO Bots (FileImageID, NameBot, Description, ShortDescription, NameForWhat, Developer, UserID)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """,

    "INSERT_IN_BOTSTYPES": """
        INSERT INTO BotsType (BotID, TypeID) VALUES (%s, %s)
    """,

    "SELECT_TYPEID": """
        SELECT TypeID FROM Type WHERE TypeName = %s
    """,

    "UPDATE_Bot": """
        UPDATE Bots SET NameBot=%s, NameForWhat=%s, Description=%s, ShortDescription=%s, Developer=%s where BotID=%s;
    """,

    "SELECT_ALL_REVIEWS": """
        SELECT
        Reviews.BotID,
        Reviews.Rating,
        Reviews.TextReviews,
        Reviews.PublicationDate,
        Users.Login
    FROM
        Reviews
    JOIN
        Users ON Reviews.UserID = Users.UserID
    WHERE
        Reviews.BotID = %s and 
        Reviews.StatusID = 2
    LIMIT %s OFFSET %s;
    """,

    "SELECT_USER_REVIEW": """
        SELECT
        Users.Login,
        Reviews.StatusID,
        Reviews.ReviewID,
        Reviews.BotID,
        Reviews.UserID,
        Reviews.Rating,
        Reviews.TextReviews,
        Reviews.PublicationDate,
        Users.FirstName,
        Users.LastName
    FROM
        Reviews
    JOIN
        Users ON Reviews.UserID = Users.UserID
    WHERE
        Users.UserID = %s AND
        Reviews.BotID = %s;
    """,
    "INSERT_REVIEW_USER": """
        INSERT INTO Reviews(BotID, UserID, Rating, TextReviews)
        VALUES (%s, %s, %s, %s);
    """,
    "SELECT_ALL_USER_REVIEWS": """
        SELECT
            Users.Login,
            Reviews.ReviewID,
            Reviews.BotID,
            Reviews.UserID,
            Reviews.Rating,
            Reviews.TextReviews,
            Reviews.PublicationDate,
            Reviews.StatusID,
            ReviewStatus.StatusName,
            Bots.NameBot,
            Users.FirstName,
            Users.LastName
        FROM
            Reviews
        JOIN
            Users ON Reviews.UserID = Users.UserID
        JOIN
            ReviewStatus ON Reviews.StatusID = ReviewStatus.StatusID
        JOIN
            Bots ON Reviews.BotID = Bots.BotID
        WHERE
            Users.UserID = %s;
    """,

    "SELECT_ALL_REVIEWS_FOR_MODERATOR": """
    SELECT
        Users.Login,
        Reviews.ReviewID,
        Reviews.BotID,
        Reviews.UserID,
        Reviews.Rating,
        Reviews.TextReviews,
        Reviews.PublicationDate,
        Reviews.StatusID,
        ReviewStatus.StatusName,
        Bots.NameBot,
        Users.FirstName,
        Users.LastName
    FROM
        Reviews
    JOIN
        Users ON Reviews.UserID = Users.UserID
    JOIN
        ReviewStatus ON Reviews.StatusID = ReviewStatus.StatusID
    JOIN
        Bots ON Reviews.BotID = Bots.BotID
    WHERE
        Reviews.StatusID = 1;
    """,

    "SELECT_ALL_REVIEW_FOR_MODERATOR": """
        SELECT
            Users.Login,
            Reviews.ReviewID,
            Reviews.BotID,
            Reviews.UserID,
            Reviews.Rating,
            Reviews.TextReviews,
            Reviews.PublicationDate,
            Reviews.StatusID,
            ReviewStatus.StatusName,
            Bots.NameBot,
            Users.FirstName,
            Users.LastName
        FROM
            Reviews
        JOIN
            Users ON Reviews.UserID = Users.UserID
        JOIN
            ReviewStatus ON Reviews.StatusID = ReviewStatus.StatusID
        JOIN
            Bots ON Reviews.BotID = Bots.BotID
        WHERE
            Reviews.ReviewID = %s;
    """,

    "UPDATE_STATUS": """
        UPDATE Reviews
        SET StatusID = %s
        WHERE ReviewID = %s;
    """,

    "INSERT_FILE": """
        INSERT INTO ImageFiles (FileID, FileName, MIMEType, MD5Hash) 
        VALUES (%s, %s, %s, %s);
    """,

    "SELECT_FILENAME": """
        SELECT ImageFiles.FileName FROM ImageFiles WHERE FileID = %s
    """
}
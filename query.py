queries = {
    'SELECT_BOT_INFO_FOR_CARD': """
            SELECT
                Bots.NameBot,
                GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
                Bots.BotID,
                Bots.ReleaseDate,
                ROUND(AVG(Reviews.Rating), 1) AS AverageRating,
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
                Bots.ReleaseDate DESC
            LIMIT %s OFFSET %s;
    """,

    'SELECT_BOT_INFO_FOR_SHOW':"""
        SELECT 
            Bots.BotID,
            Bots.NameBot,
            Bots.ShortDescription,
            Bots.Description,
            Bots.Developer,
            Bots.ReleaseDate,
            GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
            ROUND(AVG(Reviews.Rating), 1) AS AverageRating,
            COUNT(DISTINCT Reviews.ReviewID) AS ReviewCount,
            Files.FileImagePath
        FROM
            Bots
        LEFT JOIN Files ON Bots.BotID = Files.FileID
        LEFT JOIN Reviews ON Bots.BotID = Reviews.BotID
        LEFT JOIN BotsType ON Bots.BotID = BotsType.BotID
        LEFT JOIN Type ON BotsType.TypeID = Type.TypeID
        WHERE
            Bots.BotID = %s -- подставляется id бота
        GROUP BY
            Bots.BotID, Files.FileImagePath;
    """,

    "DELETE_BOT_IN_BOTS_TABLE": """
    DELETE FROM Bots WHERE BotID = %s
    """,

    "SELECT_TYPES": """
        SELECT 
            Type.TypeName
        From Type;
    """,

    "INSERT_BOT": """
    INSERT INTO Bots (NameBot, NameForWhat, Description, ShortDescription, Developer, UserID) 
    VALUES (%s, %s, %s, %s, %s, %s);
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
        Reviews.BotID = %s
    LIMIT %s OFFSET %s;
    """,

    "SELECT_USER_REVIEW": """
        SELECT
        Users.Login,
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
    """

}
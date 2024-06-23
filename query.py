queries = {
    'SELECT_BOT_INFO_FOR_CARD': """
            SELECT
                Bots.NameBot,
                GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
                Bots.BotID,
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
                Bots.ReleaseDate DESC
            LIMIT %s OFFSET %s;
    """,
    'SELECT_BOT_INFO_FOR_SHOW':"""
        SELECT 
            Bots.NameBot,
            Bots.ShortDescription,
            Bots.Description,
            Bots.Developer,
            Bots.ReleaseDate,
            GROUP_CONCAT(DISTINCT Type.TypeName SEPARATOR ', ') AS BotTypes,
            AVG(Reviews.Rating) AS AverageRating,
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
    """

}
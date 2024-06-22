queries = {
    'SELECT_BOT_INFO_FOR_CARD': """
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
    """
}
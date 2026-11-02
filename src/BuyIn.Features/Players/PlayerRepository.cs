namespace BuyIn.Features.PlayerRepository
{
    using BuyIn.Data.Config;
    using BuyIn.Features.Player;
    using BuyIn.Tools.Log;

    public class PlayerData
    {
        // the one place the player db and table names live; public so Program.cs can use them too
        public const string DbName = "BuyInPlayer.db";
        public const string TableName = "Players";

        public static Player? GetPlayerInfo(string playerId)
        {
            try
            {
                using var connection = Setup.CreateConnection(DbName);
                using var readCommand = connection.CreateCommand();
                readCommand.CommandText =
                    $"""
                    select PlayerFirstName, PlayerLastName, PlayerId from {TableName} where playerId = $playerId
                    """;
                readCommand.Parameters.AddWithValue("$playerId", playerId);
                using var reader = readCommand.ExecuteReader();

                if (reader.Read())
                {
                    string first = reader.GetString(reader.GetOrdinal("PlayerFirstName"));
                    string last = reader.GetString(reader.GetOrdinal("PlayerLastName"));
                    string id = reader.GetString(reader.GetOrdinal("PlayerId"));
                    return new Player(first, last, id);
                }
                else
                {
                    Logger.Info(body: "Player not found", resource: nameof(PlayerData), attributes: new() { ["playerId"] = playerId });
                    return null;
                }
            }
            catch (Exception e)
            {
                Logger.Error(body: "Failed to read player", resource: nameof(PlayerData), attributes: new() { ["playerId"] = playerId, ["tableName"] = TableName }, exception: e);
                throw; // plain "throw;"
            }
        }
    }
}
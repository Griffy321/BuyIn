namespace BuyIn.Data.Config
{
    using Microsoft.Data.Sqlite;
    using BuyIn.Tools.Log;

    public static class Setup
    {
        private static readonly string _dbPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "BuyInData.db");
        private static readonly string _connectionString = $"Data Source={_dbPath}";

        public static bool CreateDB()
        {
            if (!Path.Exists(_dbPath)) 
            {
                try 
                {
                    var file = File.Create(_dbPath);
                    Logger.Info(body: "Database file created", resource: nameof(Setup), attributes: new() { ["path"] = _dbPath }); // file created
                    file.Close();
                    return true;
                }
                catch (Exception ex)
                {
                    Logger.Error(body: "Failed to create database file", resource: nameof(Setup), attributes: new() { ["path"] = _dbPath }, exception: ex); // failed to make file
                    return false;
                }
            }
            else
            {
                Logger.Info(body: "Database file already exists", resource: nameof(Setup), attributes: new() { ["path"] = _dbPath }); // file exists
                return true;
            }
        }

        public static SqliteConnection CreateConnection()
        {
            Logger.Info(body: "Opening database connection", resource: nameof(Setup), attributes: new() { ["connectionString"] = _connectionString }); // making connection
            try
            {
                var connection = new SqliteConnection(_connectionString);
                connection.Open();
                Logger.Info(body: "Database connection opened", resource: nameof(Setup)); // connection open
                return connection;

            }
            catch (Exception e)
            {
                Logger.Error(body: "Failed to open database connection", resource: nameof(Setup), attributes: new() { ["connectionString"] = _connectionString }, exception: e); // failed to connect
                throw;
            }
        }
    }
}
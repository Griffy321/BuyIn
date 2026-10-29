namespace BuyIn.Data.Config
{
    using Microsoft.Data.Sqlite;
    using BuyIn.Tools.Log;

    public static class Setup
    {
        private static readonly string _dbFolder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "Database");

        private static string GetDbPath(string dbName) => Path.Combine(_dbFolder, dbName);

        private static void ValidateDbName(string dbName)
        {
            if (!dbName.EndsWith(".db"))
            {
                Logger.Warn(body: "Database name must end with .db", resource: nameof(Setup), attributes: new() { ["dbName"] = dbName }); // warn you must provide a .db
                throw new ArgumentException("dbName must end with .db", nameof(dbName));
            }
        }

        public static bool CreateDB(string dbName)
        {
            ValidateDbName(dbName);
            string dbPath = GetDbPath(dbName);
            if (!File.Exists(dbPath))
            {
                try
                {
                    Directory.CreateDirectory(_dbFolder); // does nothing if the folder already exists
                    var file = File.Create(dbPath);
                    Logger.Info(body: "Database file created", resource: nameof(Setup), attributes: new() { ["path"] = dbPath }); // file created
                    file.Close();
                    return true;
                }
                catch (Exception ex)
                {
                    Logger.Error(body: "Failed to create database file", resource: nameof(Setup), attributes: new() { ["path"] = dbPath }, exception: ex); // failed to make file
                    return false;
                }
            }
            else
            {
                Logger.Info(body: "Database file already exists", resource: nameof(Setup), attributes: new() { ["path"] = dbPath }); // file exists
                return true;
            }
        }

        public static SqliteConnection CreateConnection(string dbName)
        {
            ValidateDbName(dbName);
            string connectionString = $"Data Source={GetDbPath(dbName)};Mode=ReadWrite"; // ReadWrite errors on a missing file instead of making a new empty one
            Logger.Info(body: "Opening database connection", resource: nameof(Setup), attributes: new() { ["connectionString"] = connectionString }); // making connection
            try
            {
                var connection = new SqliteConnection(connectionString);
                connection.Open();
                Logger.Info(body: "Database connection opened", resource: nameof(Setup)); // connection open
                return connection;

            }
            catch (Exception e)
            {
                Logger.Error(body: "Failed to open database connection", resource: nameof(Setup), attributes: new() { ["connectionString"] = connectionString }, exception: e); // failed to connect
                throw;
            }
        }
    }
}

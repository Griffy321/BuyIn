namespace BuyIn.Tools.Log 
{

    using System.Text.Json;
    using BuyIn.Tools.RandomStr;
    public static class Logger
    {
        private static readonly string filePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "BuyInLogs.txt");

        public static void Info(string body, string? resource = null, Dictionary<string, object?>? attributes = null, Exception? exception = null)
        {
            Write("Info", body, resource, attributes, exception);
        }
        public static void Warn(string body, string? resource = null, Dictionary<string, object?>? attributes = null, Exception? exception = null)
        {
            Write("Warning", body, resource, attributes, exception);
        }
        public static void Error(string body, string? resource = null, Dictionary<string, object?>? attributes = null, Exception? exception = null)
        {
            Write("Error", body, resource, attributes, exception);
        }

        private static void Write(string level, string body, string? resource, Dictionary<string, object?>? attributes, Exception? exception)
        {
            var log = new Dictionary<string, object?>
            {
                ["timestamp"] = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffZ"), // utc time, ISO 8601
                ["traceID"] = RandomString.GenerateUID(), // distinct log id
                ["level"] = level, // log level
                ["body"] = body, // human readable text saying what's up
            };
            if (resource != null) {log["resource"] = resource;} // the thing that made the log, e.g. the name of the class that makes the object
            if (attributes != null) {log["attributes"] = attributes;} // details relating to the object like the playerID, written as a nested JSON object
            if (exception != null) {log["exception"] = exception.ToString();} // any exceptions go here

            try
            {
                string json = JsonSerializer.Serialize(log);
                File.AppendAllText(filePath, json + Environment.NewLine);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Failed to write log: " + ex.Message);
                Console.WriteLine(string.Join(" ", log.Values));
            }
        }
    }
}

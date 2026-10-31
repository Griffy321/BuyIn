namespace BuyIn.Data.Write
{
    using BuyIn.Data.Config;
    using System.Reflection;
    using BuyIn.Tools.Log;

    public class Insert
    {
        public Dictionary<string, object?> GetMetaData(object record)
        {
            Dictionary<string, object?> columnValues = new Dictionary<string, object?>();
            Array propertyDescriptions = record.GetType().GetProperties();
            foreach (PropertyInfo description in propertyDescriptions)
            {
                string key = description.Name;
                object? value = description.GetValue(record);
                columnValues[key] = value;
            }
            return columnValues;
        }

        public bool WriteRecord(string dbName, string tableName, object record)
        {
            Dictionary<string, object?> columnValues = GetMetaData(record);
            string columnNames = String.Join(", ", columnValues.Keys);
            string placeholders = String.Join(", ", columnValues.Keys.Select(key => "$" + key));
            try
            {
                using var connection = Setup.CreateConnection(dbName);
                using var insertCommand = connection.CreateCommand();
                insertCommand.CommandText = 
                $"""
                insert into {tableName} ({columnNames})
                values ({placeholders})
                """;
                foreach (var column in columnValues)
                {
                    insertCommand.Parameters.AddWithValue("$" + column.Key, column.Value ?? DBNull.Value);
                }
                insertCommand.ExecuteNonQuery();
                return true;
            }
            catch (Exception e)
            {
                Logger.Warn(body: "Failed to write record", resource: nameof(Insert), attributes: new() { ["tableName"] = tableName }, exception: e);
                return false;
            }
        }
    }
}

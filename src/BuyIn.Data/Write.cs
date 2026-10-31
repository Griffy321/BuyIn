namespace BuyIn.Data.Write
{
    using BuyIn.Data.Config;
    using System.Reflection;

    public class Insert
    {
        public Dictionary<string, object?> GetMetaData(object classInstance)
        {
            Dictionary<string, object?> propertieData = new Dictionary<string, object?>();
            Array classData = classInstance.GetType().GetProperties();
            Console.WriteLine(classData);
            // for (int i = 0; i < classData.Length; i++)
            // {
            //     propertieData
            // }
            return propertieData;
        }

        public bool WriteRecord(string tableName)
        {
            var connection = Setup.CreateConnection(tableName);

            return true;


        }
    }
}
